import subprocess
from django.shortcuts import get_object_or_404, get_list_or_404
from interaction.models import UserCourse, UserLesson
from courses.models import Lesson

def git_branch_render(request):
    """Obtain the active git branch and ensure it is present in template vars"""
    
    process = subprocess.Popen("cd /var/www/eduduck; git branch |grep '*' |cut -c 2-", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    agb = process.stdout.read()

    return {'ACTIVE_GIT_BRANCH': agb}

def show_survey_link(request):
    """Calculate whether to show the survey link (nominally 50% complete by some measure

    This will only work on assumption of there being one course, which is true for MVP0.1
    The entire premise will be irrelevant beyond MVP0.1"""

    #Obtain total number of lessons in course
    lessons_total = 0
    if request.user.is_authenticated():
        #All the lessons will be in the one and only course for MVP0.1
        lessons_total = len(Lesson.objects.all())
        lessons_visited = len(get_list_or_404(UserLesson, user=request.user, 
                                      visited=True))
    
    if (lessons_total==0):
        return {'COMPLETION_RATIO': 0}
    else:
        return {'COMPLETION_RATIO': 100*lessons_visited/lessons_total}

    
    
