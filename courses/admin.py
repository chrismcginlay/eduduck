# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 23:59:53 2012

@author: chris
"""

from courses.models import Course, Lesson, Video, Attachment 
from courses.models import UserProfile, UserProfile_Lesson
from quiz.models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    
class QuizAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile_Lesson)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Attachment)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuestionAttempt)
