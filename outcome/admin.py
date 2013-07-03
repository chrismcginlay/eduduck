from django.contrib import admin
from .models import LearningIntention, LearningIntentionDetail

class QuizAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

class LearningIntentionDetailInline(admin.TabularInline):
    model = LearningIntentionDetail
    
class LearningIntentionAdmin(admin.ModelAdmin):
#    readonly_fields = ("lesson",)
    inlines = [LearningIntentionDetailInline]

admin.site.register(LearningIntention, LearningIntentionAdmin)
