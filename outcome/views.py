#outcome/views.py
from django.core.exceptions import (
    ObjectDoesNotExist,
    PermissionDenied,
)
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.shortcuts import (
    get_object_or_404,
    render
)
                              
from django.template import RequestContext
from courses.models import Course
from lesson.models import Lesson
from interaction.models import (
    UserLearningIntention,
    UserLearningIntentionDetail, 
    ULIDConditions
)
from .models import LearningIntention, LearningIntentionDetail

import logging
logger = logging.getLogger(__name__)

SCInlineFormset = inlineformset_factory(
    LearningIntention, form=SCForm, extra=6)
LOInlineFormset = inlineformset_factory(
    LearningIntention, form=LOForm, extra=6)

def _user_permitted_to_edit_course(user, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not user.is_authenticated(): return False
    if not (user.id ==  course.organiser_id or user.id == course.instructor_id):
        return False
    return True

def learning_intention(request, lesson_id, learning_intention_id):
    """Prepare variables for learning intention template"""
   
    logger.info('Lesson id=' + str(lesson_id) + \
        ', Learn_Int id=' + str(learning_intention_id) + ' view')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    learning_intention = get_object_or_404(LearningIntention, 
                                           id=learning_intention_id) 
    context_data = dict()
    user_can_edit = _user_permitted_to_edit_course(
        request.user, lesson.course.id)
    if request.user.is_authenticated():
        #Construct two lists of tuples [(lid, condition ulid)] where 
        # lid = learningintentiondetail,
        # condition = 'red' | 'amber' | 'green'
        # ulid = ID of of any pre-existing user interaction with lid | None  
        #List 'usc_list' is for user's success criteria
        #List 'ulo_list' is for user's learning outcomes
        usc_list = list()
        ulo_list = list()
        userlids = request.user.userlearningintentiondetail_set.all()              
        for lid in learning_intention.learningintentiondetail_set.all():
            try:
                match = userlids.get(learning_intention_detail = lid)
                condition = match.get_status()
            except ObjectDoesNotExist:
                match = None
                condition = ULIDConditions[0] # 'red'
            if lid.lid_type == LearningIntentionDetail.SUCCESS_CRITERION:
                usc_list.append((lid, condition, match))
            else:
                ulo_list.append((lid, condition, match))

        if request.method == u"POST":
            #First see if a success_criterion type LID is cycled
            for (idx, ulid) in enumerate(usc_list):
                target = "cycle" + str(ulid[0].pk)   #which sc to cycle
                lid = ulid[0]
                if target in request.POST:  
                    if ulid[2]: #already in database
                        ulid[2].cycle()
                        newcond = ulid[2].get_status() 
                        ulid = ((lid, newcond, ulid[2]))
                    else:
                        new_ulid = UserLearningIntentionDetail(
                            learning_intention_detail=lid, 
                            user=request.user)
                        new_ulid.save()
                        new_ulid.cycle()
                        ulid = (( lid, ULIDConditions[1], new_ulid)) # amber
                    usc_list[idx] = ulid
            #Repeat, to see if a learning_outcome type LID is cycled
            for (idx, ulid) in enumerate(ulo_list):
                target = "cycle" + str(ulid[0].pk)   #which sc to cycle
                lid = ulid[0]
                if target in request.POST:  
                    if ulid[2]: #already in database
                        ulid[2].cycle()
                        newcond = ulid[2].get_status()
                        ulid = ((lid, newcond, ulid[2]))
                    else:
                        new_ulid = UserLearningIntentionDetail(
                            learning_intention_detail=lid, 
                            user=request.user)
                        new_ulid.save()
                        new_ulid.cycle()
                        ulid = (( lid, ULIDConditions[1], new_ulid))
                    ulo_list[idx] = ulid
        #Construct progress bar graph tuples (val, max-val, max, width)
        uli = UserLearningIntention.objects.get_or_create(
            user=request.user,
            learning_intention = learning_intention
        )
        #get or create produces a tuple with status (we only want 1st element)
        rawSC = uli[0].progress()[u'SC']
        rawLO = uli[0].progress()[u'LO']
        #tuples (n complete, n not complete, N, 100% width)
        progressSC = ( rawSC[0], rawSC[1]-rawSC[0], rawSC[1], 100 )
        progressLO = ( rawLO[0], rawLO[1]-rawLO[0], rawLO[1], 100 )
        if user_can_edit:
            context_data.update({
                'progressSC': None,
                'progressLO': None,
                'user_can_edit': user_can_edit,
            })
        else:
            context_data.update({
                'progressSC':  progressSC,
                'progressLO':  progressLO,
                'user_can_edit': user_can_edit,
            })
    else: #not authenticated
        usc_list = [(lid, ULIDConditions[0], None) for lid in 
            learning_intention.learningintentiondetail_set.filter(
                    lid_type = LearningIntentionDetail.SUCCESS_CRITERION)]
        ulo_list = [(lid, ULIDConditions[0], None) for lid in 
            learning_intention.learningintentiondetail_set.filter(
                    lid_type = LearningIntentionDetail.LEARNING_OUTCOME)]
    context_data.update({
                    'lesson':               lesson,
                    'learning_intention':   learning_intention,
                    'usc_list':             usc_list,
                    'ulo_list':             ulo_list,
                    'user_can_edit':        user_can_edit,
                    })
    template = 'outcome/outcome_lint.html'
    return render(request, template, context_data)

@login_required
def edit(request, lesson_id, learning_intention_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course.id
    if _user_permitted_to_edit_course(request.user, course_id):
        li_form = None
        sc_formset = None
        lo_formset = None
        t = 'outcome/edit_lint.html'
        c = {
            'li_form': li_form,
            'sc_formset': sc_formset,
            'lo_formset': lo_formset,
        }
        return render(request, t, c)   
    else:
        logger.info("Unauthorized attempt to edit "\
            "learning_intention {0}".format(learning_intention_id))
        raise PermissionDenied
