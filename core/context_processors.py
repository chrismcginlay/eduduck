import subprocess
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from interaction.models import UserCourse, UserLesson
from lesson.models import Lesson

def git_branch_render(request):
    """Obtain the active git branch and ensure it is present in template vars"""
    
    cmd_str = "cd {0}; git branch |grep '*' |cut -c 2-".format(
        settings.SITE_ROOT)
    process = subprocess.Popen(cmd_str,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT
                               )
    agb = process.stdout.read()

    return {'ACTIVE_GIT_BRANCH': agb}

