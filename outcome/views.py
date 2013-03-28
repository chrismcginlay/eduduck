from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (render_to_response, 
                              get_object_or_404)
                              
from django.template import RequestContext
from courses.models import Lesson
from outcome.models import LearningIntention

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
                                          
    #Construct list of tuples usc[(sc, condition)] where condition = red etc
    usc = list()
    usercriteria = request.user.usersuccesscriterion_set.all()
    for succcrit in learning_intention.successcriterion_set.all():
        try:
            match = usercriteria.get(success_criterion = succcrit)
            offset = match.condition * -17
        except ObjectDoesNotExist:
            match = None
            offset = 0
        usc.append((succcrit, offset))
    
    template = 'outcome/outcome_lint.html'
    context_data =  {
                    'lesson':   lesson,
                    'learning_intention': learning_intention,
                    'usc':  usc
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
   