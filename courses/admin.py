from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from courses.models import Course

from profile.models import Profile
from quiz.models import Quiz, Question, Answer, QuizAttempt, QuestionAttempt


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'
    
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

class QuizAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ("taken_dt",)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Course)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuestionAttempt)
