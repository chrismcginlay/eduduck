#For django-haystack and elasticsearch
import datetime
from haystack import indexes
from courses.models import Course, Lesson, Video

class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='course_organiser')
    course_code = indexes.CharField(model_attr='course_code')
    course_abstract = indexes.CharField(model_attr='course_abstract')

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class LessonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    abstract = indexes.CharField(model_attr='abstract')
    
    def get_model(self):
        return Lesson

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    video_pk = indexes.CharField(model_attr='pk')
    
    def get_model(self):
        return Video

    def index_querset(self, using=None):
        return self.get_model().objects.all()
