#Testing#

##There are functional tests. Run using the test settings. Run them against 
##your development environment and against staging:
    
`python manage.py test functional_tests --settings=EduDuck.settings.test`
`python manage.py test functional_tests --liveserver=staging.eduduck.com --settings=EduDuck.settings.test`

If you would like to add or edit the fixtures for functional_tests, you will 
find them in JSON format in functional_tests/fixtures. Note that if adding new
users to the auth_user.json, you'll need to generate a hashed password:
    >>> from django.contrib.auth.models import User
    >>> u = User()
    >>> u.set_password('newpass')
    >>> u.password
    
##There are unittests which should be...##

1. added to if adding new code or changing functionality
2. added to if implementing a bug-fix. Your test should reproduce the bug
3. executed after working on code
4. executed before merging to master

##Unit tests at present, and how to run them:##
`python manage.py test courses --settings=EduDuck.settings.test`
`python manage.py test interaction --settings=EduDuck.settings.test`
`python manage.py test bio --settings=EduDuck.settings.test`
`python manage.py test outcome --settings=EduDuck.settings.test`
`python manage.py test support --settings=EduDuck.settings.test`
`python manage.py test attachment --settings=EduDuck.settings.test`

Or just run them all:
    `python manage.py test courses interaction bio outcome support attachment --settings=EduDuck.settings.test`

##WARNING status in logs after running tests##
Because the tests intentionally subject the models to failure cases, the tests 
check that the models raise correct errors and log correct messages.
Therefore logs will show 
`WARNING [interaction.models:79] UC Checkrep failed`
..or similar during test runs. This means that _checkrep is picking up the 
failing state correctly when presented with an inconsistent state in tests.
Obviously, we don't want to see such errors during production or even dev runs.
