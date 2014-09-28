# Test the course urls
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
    def test_all_course_index(self):
        url = reverse('course_index')
        self.assertEqual(url, '/courses/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_index')
    
    def test_course_single(self):
        url = reverse('course_single', args=[1])
        self.assertEqual(url, '/courses/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_single')
        self.assertEqual(resolver.kwargs, {'course_id': '1'})
        
    def test_course_lesson(self):
        url = reverse('course_lesson', args=[1,1])
        self.assertEqual(url, '/courses/1/lesson/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'lesson_view')
        self.assertEqual(resolver.kwargs, {'course_id': '1', 'lesson_id': '1'})
        
    def test_course_create(self):
        url = reverse('course_create')
        self.assertEqual(url, '/courses/create/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_create')
        
    def test_course_edit(self):
        url = reverse('course_edit', kwargs={'course_id': 1})
        self.assertEqual(url, '/courses/1/edit/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_edit')
        self.assertEqual(resolver.kwargs, {'course_id': '1'})
