from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404
from django.contrib.auth.models import User
from profile.models import Profile 


class Course(models.Model):
    """A self contained course of study.
    
    Attributes:
        code         Optional. Course code for human consumption
        name         Human readable name of course
        abstract     Summary paragraph outlining course
        organiser    Foreign key: user organising course
        instructor   Foreign key: user providing instruction 
    """

    code = models.CharField(max_length=10,
                            help_text="optional course code for "\
                            	      "author's reference",
                            blank=True)
    name = models.CharField(max_length=20,
                            help_text="human readable short name of the course")
    abstract = models.TextField(help_text="summary of the course "\
                                	  "in a couple of paragraphs")
    organiser = models.ForeignKey(User,
                                  related_name="courses_organised_set",
                                  help_text="This user is organising the course")
    instructor = models.ForeignKey(User,
                                   related_name="courses_instructed_set",
                                   help_text="This user is providing the instruction")

    def __init__(self, *args, **kwargs):
        super (Course, self).__init__(*args, **kwargs)
        #When adding a new instance (e.g. in admin), their will be no 
        #datamembers, so only check existing instances eg. from db load.
        if self.pk != None:
            self._checkrep()

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        assert self.id >=1
        return reverse(u"courses.views.detail", kwargs= {'course_id': self.id})

    def save(self, *args, **kwargs):
        self._checkrep()
        super(Course, self).save(*args, **kwargs)
        
    def _checkrep(self):
        assert self.name
        assert self.organiser
        assert self.instructor
