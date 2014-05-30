from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (render_to_response, 
                              get_object_or_404)
                              
from django.template import RequestContext
from lesson.models import Lesson
from interaction.models import (
    UserLearningIntention,
    UserLearningIntentionDetail, 
    ULIDConditions
)
from .models import LearningIntention, LearningIntentionDetail

import logging
logger = logging.getLogger(__name__)


def learning_intention(request, lesson_id, learning_intention_id):
    """Prepare variables for learning intention template"""
    
    logger.info('Lesson id=' + str(lesson_id) + \
        ', Learn_Int id=' + str(learning_intention_id) + ' view')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    learning_intention = get_object_or_404(LearningIntention, 
                                           id=learning_intention_id) 
    context_data = dict()
    if request.user.is_authenticated():
        #Construct two lists of tuples [(lid, condition)] where 
        #lid = learningintentiondetail and condition = red etc. 
        #List 'usc_list' is for user's success criteria
        #List 'ulo_list' is for user's learning outcomes
        usc_list = list()
        ulo_list = list()
        userlids = request.user.userlearningintentiondetail_set.all()              
        for lid in learning_intention.learningintentiondetail_set.all():
            try:
                match = userlids.get(learning_intention_detail = lid)
                offset = match.condition * -17
            except ObjectDoesNotExist:
                match = None
                offset = 0
            if lid.lid_type == LearningIntentionDetail.SUCCESS_CRITERION:
                usc_list.append((lid, offset, match))
            else:
                ulo_list.append((lid, offset, match))

        if request.method == u"POST":
            #First see if a success_criterion type LID is cycled
            for (idx, ulid) in enumerate(usc_list):
                target = "cycle" + str(ulid[0].pk)   #which sc to cycle
                lid = ulid[0]
                if target in request.POST:  
                    if ulid[2]: #already in database
                        ulid[2].cycle()
                        #magic 17 is pixel offset for traffic light CSS prop.
                        newcond = ulid[2].condition * -17
                        ulid = ((lid, newcond, ulid[2]))
                    else:
                        new_ulid = UserLearningIntentionDetail(
                            learning_intention_detail=lid, 
                            user=request.user)
                        new_ulid.save()
                        new_ulid.cycle()
                        ulid = (( lid, -17, new_ulid))
                    usc_list[idx] = ulid
            #Repeat, to see if a learning_outcome type LID is cycled
            for (idx, ulid) in enumerate(ulo_list):
                target = "cycle" + str(ulid[0].pk)   #which sc to cycle
                lid = ulid[0]
                if target in request.POST:  
                    if ulid[2]: #already in database
                        ulid[2].cycle()
                        #magic 17 is pixel offset for traffic light CSS prop.
                        newcond = ulid[2].condition * -17
                        ulid = ((lid, newcond, ulid[2]))
                    else:
                        new_ulid = UserLearningIntentionDetail(
                            learning_intention_detail=lid, 
                            user=request.user)
                        new_ulid.save()
                        new_ulid.cycle()
                        ulid = (( lid, -17, new_ulid))
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
        context_data.update({
            'progressSC':  progressSC,
            'progressLO':  progressLO
        })
    else: #not authenticated
        usc_list = [(lid, 0, None) for lid in 
            learning_intention.learningintentiondetail_set.filter(
                    lid_type = LearningIntentionDetail.SUCCESS_CRITERION)]
        ulo_list = [(lid, 0, None) for lid in 
            learning_intention.learningintentiondetail_set.filter(
                    lid_type = LearningIntentionDetail.LEARNING_OUTCOME)]
    context_data.update({
                    'lesson':               lesson,
                    'learning_intention':   learning_intention,
                    'usc_list':             usc_list,
                    'ulo_list':             ulo_list
                    })
    template = 'outcome/outcome_lint.html'
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
   
