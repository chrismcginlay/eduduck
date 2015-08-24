#courses/tests/factories.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from factory import (
    Factory,
    PostGenerationMethodCall,
    RelatedFactory,
    Sequence,
    SubFactory,
)
from factory.django import DjangoModelFactory
from profile.models import Profile, create_profile
from ..models import Course

class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile
    
    timezone = u"UTC"
    accepted_terms = True
    signature_line = u"Testing too many things"
    user = SubFactory('courses.tests.factories.UserFactory', profile=None) 

class UserFactory(Factory):
    class Meta:
        model = User

    username = Sequence(lambda n: 'testuser{0}'.format(n))
    email = '{0}@example.com'.format(username)
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal"""

        post_save.disconnect(create_profile, User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_profile, User)
        return user

class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    code = u'TEST1'
    name = u'Tour Skiing'
    abstract = u'Learn the basics of Nordic tour skiing.'
    organiser = SubFactory(UserFactory, profile=None) 
    instructor = organiser
