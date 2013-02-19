from django.db import models

from django.contrib.auth.models import User

from courses.models import Course

class UserCourse(models.Model):
    """Track users interactions with courses.
    
    Attributes:
        course
        user
        registered  User is registered on this course. T/F
        active      User is actively engaged on this course. T/F
        withdrawn   User withdrew after registration, prior to completion. T/F
        complete    User marked course complete. 
        action      List of tuples of (datetime, action) taken 
                    eg register/complete/withdraw/reopen). Order by date.

    """
    
    course = models.ForeignKey(Course, 
        help_text="Course user is referring to")
    user = models.ForeignKey(User, 
        help_text="User interacting with course")
    
    class Meta:
        unique_together = (course, user)
        
    """register(): registered true, active true
    withdraw(): registered true, active false
    complete(): registered true, active false, complete true
    reopen(): registered true, active true, complete false
    """
