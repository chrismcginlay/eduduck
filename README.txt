EduDuck experimental course delivery platform.
Coded with Python/Django
by Chris McGinlay

**This project provides the rudiments of an Online Course Delivery Platform**.
- Several elements of such a platform are missing, such as assessment tools. If you want to use it, you'll really need to be prepared to contribute back to it, which is of course exactly what I would like to see, having brought the project to version 0.4 on my own.
- There are still many references to my particular installation setup under my workstation user name of 'chris'.
- There is an automated installer for development boxes, staging and production.

See the install.txt file for install instructions.

#Security check#
Run this on branched code prior to merge with master
```python manage.py check --deploy

#Git tag releases#

When ready to push a new tag release (e.g MVP0.3) on to production site, tag the codebase as follows

1. git tag -f LIVE #force re-use of LIVE tag on local repo
2. export TAG=`date +DEPLOYED-%F/%H%M`
3. expport MVPTAG=mvp_x.y.z_name
4. git tag $TAG
5. git tag $MVPTAG
5. git push origin :refs/tags/LIVE #delete LIVE tag from remote repo
6. git push origin LIVE $TAG $MVPTAG

#Need to Create Fixtures?#
We're still using some test fixtures, although some tests use FactoryBoy which is better.


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

