EduDuck experimental course delivery platform.
Coded with Django
by Chris McGinlay

#Create Fixtures with DumpData#

Do it thusly:

1. Store sets of fixtures together in a directory under fixtures. Could be 
sensible to name directories by date ddmmyy.

mkdir fixtures/ddmmyy
cd fixtures/ddmmyy

2. Dump each app

django-admin.py dumpdata --settings=EduDuck.settings --indent=4 
    courses > courses_data_110213.json --pythonpath='/home/chris/eduduck/'


