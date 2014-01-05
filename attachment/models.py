#Attachment/models.py
from django.db import models
from django.core.urlresolvers import reverse
from courses.models import Course, Lesson

#TODO important to validate uploaded files
#see PDF p796.
class Attachment(models.Model):
    """Handle all forms of attachment except video.
    
    Attributes:
        name        Human readable name of the attachment
        lesson      ForeignKey - if attachment embedded in lesson
        course      ForeignKey - if attachment embedded in course
        desc        Paragraph describing contents of attachment
        seq         Optional unique sequence number of attachment
        attachment  Django file model instance

    """
    
    name = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    seq = models.IntegerField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments')
    
    class Meta:
        unique_together = (("lesson", "seq"), ("course", "seq"))   

    def _checkrep(self):
        assert self.name
        assert self.attachment
        assert (self.lesson or self.course, "Attach to lesson or course!")

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Attachment, self).__init__(*args, **kwargs)
        if self.pk != None:
            self._checkrep()
    
    def __str__(self):
        """Human readable summary"""

        return u"Attachment %s, '%s...'" % (self.pk, self.name[:10])
        
    def __unicode__(self):
        """Summary for internal use"""

        return u"Att. ID:%s, '%s...'" % (self.pk, self.name[:10])   

    def get_absolute_url(self):
        """Canonical URL. Returns url for download via webserver"""
        
        assert self.id
        return self.attachment.url
        
    def get_loggable_url(self):
        """Get a URL which will allow download to be logged.
        
        Couples to interaction module.
        """
        
        assert self.id
        assert self.attachment

        return reverse(u"interaction.views.attachment_download",
                       kwargs= {'att_id': self.id})
                
    def get_metadata_url(self):
        """Provide URL for viewing attachment metadata"""
        
        assert self.id
        return reverse('attachment.views.metadata', kwargs={'att_id': self.id}) 
