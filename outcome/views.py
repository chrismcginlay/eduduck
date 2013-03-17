def learning_intention(request, lesson_id, learning_intention_id):
    """Prepare variables for learning intention template"""
    
    logger.info('Lesson id=' + str(lesson_id) + \
        ', Learn_Int id=' + str(learning_intention_id) + ' view')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    learning_intention = get_object_or_404(LearningIntention, 
                                           id=learning_intention_id) 
    
    template = 'courses/course_lint.html'
    context_data =  {
                    'lesson':  lesson,
                    'learning_intention': learning_intention,
                    }
    context_instance = RequestContext(request)
    return render_to_response(template, context_data, context_instance)
   