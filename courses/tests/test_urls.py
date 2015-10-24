#courses/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
    def test_all_course_index(self):
        url = reverse('course_index')
        self.assertEqual(url, '/courses/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_index')
    
    def test_course_detail(self):
        url = reverse('course_detail', args=[1])
        self.assertEqual(url, '/courses/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_detail')
        self.assertEqual(resolver.kwargs, {'course_id': '1'})
        
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

    def test_course_enrol(self):
        url = reverse('course_enrol', kwargs={'course_id': 1})
        self.assertEqual(url, '/courses/1/enrol/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_enrol')
        self.assertEqual(resolver.kwargs, {'course_id': '1'})

    def test_course_publish(self):
        url = reverse('course_publish', kwargs={'course_id': 1})
        self.assertEqual(url, '/courses/1/publish/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'course_publish')
        self.assertEqual(resolver.kwargs, {'course_id': '1'})

