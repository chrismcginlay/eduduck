from django.conf import settings

def git_branch_render(request):
    """Obtain the active git branch and ensure it is present in template vars"""
    return {'ACTIVE_GIT_BRANCH': settings.ACTIVE_GIT_BRANCH}
