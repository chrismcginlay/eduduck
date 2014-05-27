from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from courses.models import Course, Lesson
from video.models import Video

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

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Video)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
admin.site.register(QuestionAttempt)
