from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from courses.models import (
    Course, Lesson, Video, Attachment,
    LearningIntention, SuccessCriterion, LearningOutcome
    )
from bio.models import Bio
from quiz.models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt


class UserBioInline(admin.StackedInline):
    model = Bio
    can_delete = False
    verbose_name_plural = 'bios'
    
class UserAdmin(UserAdmin):
    inlines = (UserBioInline, )
    
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
