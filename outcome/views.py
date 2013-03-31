from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (render_to_response, 
                              get_object_or_404)
                              
from django.template import RequestContext
from courses.models import Lesson
from outcome.models import LearningIntention
from interaction.models import UserSuccessCriterion

import logging
logger = logging.getLogger(__name__)

import pdb

def learning_intention(request, lesson_id, learning_intention_id):
    """Prepare variables for learning intention template"""
    
    logger.info('Lesson id=' + str(lesson_id) + \
        ', Learn_Int id=' + str(learning_intention_id) + ' view')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    learning_intention = get_object_or_404(LearningIntention, 
                                           id=learning_intention_id) 
    if request.user.is_authenticated():
        #Construct list of tuples usc[(sc, condition)] where condition = red etc
        usc_list = list()
        usercriteria = request.user.usersuccesscriterion_set.all()              
        for succcrit in learning_intention.successcriterion_set.all():
            try:
                match = usercriteria.get(success_criterion = succcrit)
                offset = match.condition * -17
            except ObjectDoesNotExist:
                match = None
                offset = 0
            usc_list.append((succcrit, offset, match))

        if request.method == "POST":
            for (idx, usc) in enumerate(usc_list):
                target = "cycle" + str(usc[0].pk)   #which sc to cycle
                succcrit = usc[0]
                if target in request.POST:  
                    if usc[2]: #already in database
                        usc[2].cycle()
                        #magic 17 is pixel offset for traffic light CSS prop.
                        newcond = usc[2].condition * -17
                        usc = ((succcrit, newcond, usc[2]))
                    else:
                        new_usc = UserSuccessCriterion(
                            success_criterion=succcrit, 
                            user=request.user)
                        new_usc.save()
                        usc = (( succcrit, -17, new_usc))
                    usc_list[idx] = usc
    else: #not authenticated
        usc_list = [(sc, 0, None) for sc in learning_intention.successcriterion_set.all()]
    context_data =  {
                    'lesson':   lesson,
                    'learning_intention': learning_intention,
                    'usc_list':  usc_list
                    }
    template = 'outcome/outcome_lint.html'
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
   