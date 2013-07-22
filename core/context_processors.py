import subprocess

def git_branch_render(request):
    """Obtain the active git branch and ensure it is present in template vars"""
    
    process = subprocess.Popen("cd /var/www/eduduck; git branch |grep '*' |cut -c 2-", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    agb = process.stdout.read()

    return {'ACTIVE_GIT_BRANCH': agb}
