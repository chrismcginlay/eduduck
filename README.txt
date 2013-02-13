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
    courses > courses_data_ddmmyy.json --pythonpath='/home/chris/eduduck/'

Remember to dump auth.User too.

3. Dump the entire database if desired, which can later be used as
 initial_data for auto reload on syncdb. Maybe remove session data

django-admin.py dumpdata --settings=EduDuck.settings --indent=4
    eduduck_data_ddmmyy.json --pythonpath='/home/chris/eduduck/'

#Arrange to have the fixtures loaded#

0. This is for data reload with same schema.
1. Change the symlink under fixtures/initial_data.json to point to the 
directory/eduduck_ddmmyy.json file required
2. Run syncdb to stamp on existing data and replace with initial_data

OR

0. This is for schema alteration
1. mv EduDuck.db EduDuck.db.bak
2. python manage.py syncdb
3. Edit JSON files to suit new schema
4. django-admin.py loaddata --settings=EduDuck.settings 
	--pythonpath='/home/chris/eduduck/' 
	fixtures/ddmmyy/auth_user_data_ddmmyy.json
5. repeat 4 for each JSON
