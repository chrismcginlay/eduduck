# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 23:59:53 2012

@author: chris
"""

from courses.models import Course, Lesson, Video, Attachment 
from courses.models import UserProfile, UserProfile_Lesson
from quiz.models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt
from django.contrib import admin

class QuizAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Attachment)
admin.site.register(UserProfile)
admin.site.register(UserProfile_Lesson)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuestionAttempt)