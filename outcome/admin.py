from django.contrib import admin
from .models import (LearningIntention, 
                            SuccessCriterion, 
                            LearningOutcome)

class QuizAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

class SuccessCriterionInline(admin.TabularInline):
    model = SuccessCriterion
    
class LearningOutcomeInline(admin.StackedInline):
    model = LearningOutcome
    
class LearningIntentionAdmin(admin.ModelAdmin):
    readonly_fields = ("lesson",)
    inlines = [SuccessCriterionInline, LearningOutcomeInline]

admin.site.register(LearningIntention, LearningIntentionAdmin)
