from django.contrib import admin

from .models import UserCourse

class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'course', 'active')
    list_filter = ('user', 'course')
    search_fields = ('user', 'course')
    fields = (('user', 'course'), 'active', 'completed', 'withdrawn', 'history')
    readonly_fields = ('user', 'course', 'active', 'completed', 'withdrawn', 'history')

admin.site.register(UserCourse, UserCourseAdmin)