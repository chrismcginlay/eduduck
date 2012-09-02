# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 23:59:53 2012

@author: chris
"""

from courses.models import Course, Lesson, Video, Attachments 
from courses.models import UserProfile, UserProfile_Lesson
from quiz.models import Quiz, Question, Answer, Attempt
from django.contrib import admin

class AttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Attachments)
admin.site.register(UserProfile)
admin.site.register(UserProfile_Lesson)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Attempt, AttemptAdmin)