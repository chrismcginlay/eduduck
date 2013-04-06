from django.contrib import admin

from .models import UserCourse, UserLesson, UserLearningIntentionDetail

class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course', 'active')
    list_filter = ('user', 'course')
    search_fields = ('user', 'course')
    fields = (('user', 'course'), 'active', 'completed', 'withdrawn', 'history')
    readonly_fields = ('user', 'course', 'active', 'completed', 'withdrawn', 'history')

class UserLessonAdmin(admin.ModelAdmin):
    list_filter = ('user', 'lesson', 'completed')
    search_fields = ('user', 'lesson')
    readonly_fields = ('user', 'lesson', 'visited', 
                       'completed', 'history', 'note')
    
class UserLearningIntentionDetailAdmin(admin.ModelAdmin):
    list_filter = ('user', 'condition')
    search_fields = ('user', 'learning_intention_detail')
    readonly_fields = ('user', 'learning_intention_detail', 'condition', 'history')
    
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserLesson, UserLessonAdmin)
admin.site.register(UserLearningIntentionDetail, 
                    UserLearningIntentionDetailAdmin)