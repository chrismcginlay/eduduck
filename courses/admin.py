from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from courses.models import (
    Course, Lesson, Video, Attachment, UserProfile, UserProfile_Lesson,
    LearningIntention, SuccessCriterion, LearningOutcome
    )
from quiz.models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    
class QuizAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

class SuccessCriterionInline(admin.TabularInline):
    model = SuccessCriterion
    
class LearningOutcomeInline(admin.StackedInline):
    model = LearningOutcome
    
class LearningIntentionAdmin(admin.ModelAdmin):
    inlines = [SuccessCriterionInline, LearningOutcomeInline]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile_Lesson)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Attachment)
admin.site.register(LearningIntention, LearningIntentionAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuestionAttempt)
