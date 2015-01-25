#Testing#

##Coverage Report##
It is easy to generate a coverage report:

```
coverage run --source='./courses' manage.py test courses --settings=EduDuck.settings.test
coverage run --source='.' manage.py test --settings=EduDuck.settings.test
```

The first of the above will generate coverage data on the courses tests, 
whereas the second will test everything. Try `coverage report`, or, add htmlcov to .gitignore and try `coverage html`

##Functional Tests##
There are functional tests. Run using the test settings. Run them against 
your development environment and against staging:
    
```
python manage.py test functional_tests --settings=EduDuck.settings.test
python manage.py test functional_tests --liveserver=staging.eduduck.com --settings=EduDuck.settings.test
```

Run a subset of tests as follows:
```
python manage.py test functional_tests.test_account_login_logout_etc.NewVisitorDecidesToRegisterViaEmail --settings=EduDuck.settings.test
```

If you would like to add or edit the fixtures for functional_tests, you will 
find them in JSON format in functional_tests/fixtures. Note that if adding new
users to the auth_user.json, you'll need to generate a hashed password:
```
    >>> from django.contrib.auth.models import User
    >>> u = User()
    >>> u.set_password('newpass')
    >>> u.password
```    

##There are unittests which should be...##

1. added to if adding new code or changing functionality
2. added to if implementing a bug-fix. Your test should reproduce the bug
3. executed after working on code
4. executed before merging to master

##Unit tests at present, and how to run them:##
```
python manage.py test courses --settings=EduDuck.settings.test
python manage.py test interaction --settings=EduDuck.settings.test
python manage.py test profile --settings=EduDuck.settings.test
python manage.py test outcome --settings=EduDuck.settings.test
python manage.py test support --settings=EduDuck.settings.test
python manage.py test attachment --settings=EduDuck.settings.test
```
Or just run them all:
    `python manage.py test courses interaction profile outcome support attachment --settings=EduDuck.settings.test`

##Test With Sqlite3 or MySQL##
Running tests by specifying `--settings=EduDuck.settings.test` will run tests against sqlite3 database. Do this most of time for speed.

Running tests with no settings file `python manage.py test courses` will run with the default dev.py settings from `EduDuck/settings/dev.py`. This will use a MySQL database for testing which will take a bit longer
