from django.db import models

from django.contrib.auth.models import User

from courses.models import Course

class UserCourse(models.Model):
    """Track users interactions with courses.
    
    Attributes:
        course
        user
        registered
        completed
        withdrawn
        action      What the user just did (reg/complete/withdraw/reopen)
        dt          Data and time of interaction
        
    """
    
    course = models.ManyToManyField(Course, 
        help_text="Course user is referring to")
    user = models.ForeignKey(User, 
        help_text="User interacting with course")
    
    #note
    
    """Course module should have methods as follows firing updates in this
    module
    
    register(): registered true
    withdraw(): registered false
    complete(): registered true, completed true
    reopen(): registered true, completed false
    
    these would 