#attachment/models.py
from django.db import models
from django.core.urlresolvers import reverse
from courses.models import Course, Lesson

import logging
logger = logging.getLogger(__name__)

#TODO important to validate uploaded files
#see PDF p796.
class Attachment(models.Model):
    """Handle all forms of attachment except video.
    
    Attributes:
        att_code    Attachment code for human consumption
        att_name    Human readable name of the attachment
        lesson      ForeignKey - if attachment embedded in lesson
        course      ForeignKey - if attachment embedded in course
        att_desc    Paragraph describing contents of attachment
        att_seq     Optional unique sequence number of attachment
        attachment  Django file model instance

    """
    
    att_code = models.CharField(max_length=10, blank=True, null=True)
    att_name = models.CharField(max_length=200)
    lesson = models.ForeignKey(Lesson, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True)
    att_desc = models.TextField(blank=True, null=True)
    att_seq = models.IntegerField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments')
    
    class Meta:
        unique_together = (("lesson", "att_seq"), ("course", "att_seq"))   

    def _checkrep(self):
        assert self.att_code
        assert self.att_name
        assert self.attachment
        assert (self.lesson or self.course, "Attach to lesson or course!")

    def __init__(self, *args, **kwargs):
        """checkrep on instantiation"""
        super (Attachment, self).__init__(*args, **kwargs)
        if self.pk != None:
            self._checkrep()
    
    def __str__(self):
        """Human readable summary"""
        return u"Attachment %s, '%s...'" % (self.att_code, self.att_name[:10])           
        
    def __unicode__(self):
        """Summary for internal use"""
        return u"Att. ID:%s, code:%s, '%s...'" %\
            (self.pk, self.att_code, self.att_name[:10])   
            
    def get_absolute_url(self):
        """Canonical URL. Will download the attachment via intermediary view"""
        
        assert self.id        
        return reverse('interaction.attachment.views.download', (), 
                {'att_id': self.id})
                
    def get_metadata_url(self):
        """Provide URL for viewing attachment metadata"""
        
        assert self.id
        return reverse('attachment.views.metadata', (), {'att_id': self.id}) 
        
