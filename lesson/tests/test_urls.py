# Test the lesson urls
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
        
    def test_lesson_view(self):
        url = reverse('lesson_view', args=[1,1])
        self.assertEqual(url, '/courses/1/lesson/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_lesson')
        self.assertEqual(resolver.kwargs, 
            {'course_id': '1', 'lesson_id': '1'})
        
    def test_lesson_edit(self):
        url = reverse('lesson_edit', kwargs={'course_id': 1})
        self.assertEqual(url, '/courses/1/lesson/1/edit/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'lesson_edit')
        self.assertEqual(resolver.kwargs, 
            {'lesson_id': '1', 'course_id': '1'})
