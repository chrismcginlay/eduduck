#Testing#

##There are unittests which should be...##

1. added to if adding new code or changing functionality
2. added to if implementing a bug-fix. Your test should reproduce the bug
3. executed after working on code
4. executed before merging to master

##Unit tests at present, and how to run them:##
`python manage.py test courses --settings=Eduduck.settings.test`
`python manage.py test interaction --settings=Eduduck.settings.test`
`python manage.py test bio --settings=Eduduck.settings.test`
`python manage.py test outcome --settings=Eduduck.settings.test`
`python manage.py test support --settings=Eduduck.settings.test`

##WARNING status in logs after running tests##
Because the tests intentionally subject the models to failure cases, the tests 
check that the models raise correct errors and log correct messages.
Therefore logs will show 
`WARNING [interaction.models:79] UC Checkrep failed`
..or similar during test runs. This means that _checkrep is picking up the 
failing state correctly.
Obviously, we don't want to see such errors during production or even dev runs.
