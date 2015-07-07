EduDuck experimental course delivery platform.
Coded with Django
by Chris McGinlay

#Git tag releases

When ready to push a new tag release (e.g MVP0.3) on to production site, tag the codebase as follows

1. git tag -f LIVE #force re-use of LIVE tag on local repo
2. export TAG=`date +DEPLOYED-%F/%H%M`
3. expport MVPTAG=mvp_x.y.z_name
4. git tag $TAG
5. git tag $MVPTAG
5. git push origin :refs/tags/LIVE #delete LIVE tag from remote repo
6. git push origin LIVE $TAG $MVPTAG

#Create Fixtures with DumpData#

Do it thusly:

1. Store sets of fixtures together in a directory under fixtures. Could be 
sensible to name directories by date ddmmyy.

mkdir fixtures/ddmmyy
cd fixtures/ddmmyy

2. Dump each app

django-admin.py dumpdata --settings=EduDuck.settings --indent=4 
    courses > courses_data_ddmmyy.json --pythonpath='/home/chris/eduduck/'

Remember to dump auth.User too.

3. Dump the entire database if desired. Maybe remove session data

django-admin.py dumpdata --settings=EduDuck.settings --indent=4
    eduduck_data_ddmmyy.json --pythonpath='/home/chris/eduduck/'

