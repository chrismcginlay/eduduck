import subprocess
from interaction.models import UserCourse, UserLesson
from courses.models import Lesson

def git_branch_render(request):
    """Obtain the active git branch and ensure it is present in template vars"""
    
    process = subprocess.Popen("cd /var/www/eduduck; git branch |grep '*' |cut -c 2-", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    agb = process.stdout.read()

    return {'ACTIVE_GIT_BRANCH': agb}

def show_survey_link(request):
    """Calculate whether to show the survey link (nominally 50% complete by some measure"""

    #Obtain total number of lessons in course
    course = UserCourse.filter(user=request.user)
    lessons_total = Lesson.objects.filter(course=course) 
    lessons_visited = UserLesson.objects.filter(user = request.user, visited=True).count
    
    if (lessons_total==0):
        return {'COMPLETION_RATIO': 0}
    else:
        return {'COMPLETION RATIO': lessons_visited/lessons_total}

    
    
