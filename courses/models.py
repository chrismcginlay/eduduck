from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from checkout.models import PricedItem
from profile.models import Profile 


class Course(models.Model):
    """A self contained course of study.
    
    Attributes:
        code         Optional. Course code for human consumption
        name         Human readable name of course
        abstract     Summary paragraph outlining course
        published    Boolean. True if published. Default False
        organiser    Foreign key: user organising course
        instructor   Foreign key: user providing instruction 
    """

    class Meta:
        permissions = (
            ("study_course", "User can enrol and study this course"),
        )
    
    code = models.CharField(
        max_length=10,
        help_text="optional course code for author's reference",
        blank=True
    )
    name = models.CharField(
        max_length=20,
        help_text="human readable short name of the course"
    )
    abstract = models.TextField(
        help_text="summary of the course in a couple of paragraphs"
    )
    published = models.BooleanField(
        default = False,
        blank = False,
        null = False
    )
    organiser = models.ForeignKey(
        User,
        related_name="courses_organised_set",
        help_text="This user is organising the course"
    )
    instructor = models.ForeignKey(
        User,
        related_name="courses_instructed_set",
        help_text="This user is providing the instruction"
    )

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
        super(Course, self).save(*args, **kwargs)
        course_type = ContentType.objects.get_for_model(Course)
        (pitem, created) = PricedItem.objects.get_or_create(
            content_type_id = course_type.pk,
            object_id=self.pk
        )
        self._checkrep()
        
    def _checkrep(self):
        assert self.name
        assert self.organiser
        assert self.instructor
        course_type = ContentType.objects.get_for_model(Course)
        pitem = PricedItem.objects.get_or_create(
            content_type_id = course_type.pk,
            object_id=self.pk
        )
