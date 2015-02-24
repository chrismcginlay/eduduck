#interaction/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
    def test_attachment_download(self):
        url = reverse('attachment_download', kwargs={'att_id':1})
        self.assertEqual(url, '/interaction/attachment/1/download/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'attachment_download')
    
    def test_usercourse_single(self):
        url = reverse('usercourse_single', args=[1,2])
        self.assertEqual(url, '/interaction/user/1/courses/2/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'usercourse_single')
        self.assertEqual(resolver.kwargs, 
            {'course_id': '2', 'user_id': '1'})

    def test_userlesson_single(self):
        url = reverse('userlesson_single', args=[1,2])
        self.assertEqual(url, '/interaction/user/1/lesson/2/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'userlesson_single')
        self.assertEqual(resolver.kwargs,
            {'lesson_id': '2', 'user_id': '1'})

    def test_userlearningintentiondetail_single(self):
        url = reverse('userlearningintentiondetail_single', args=[1,2])
        self.assertEqual(url, '/interaction/user/1/learningintentiondetail/2/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'userlearningintentiondetail_single')
        self.assertEqual(resolver.kwargs,
            {'user_id': '1', 'lid_id': '2'})

    def test_ajax_userlearningintentiondetail_status(self):
        url = reverse('ajax_learningintentiondetail_status', args=[1])
        self.assertEqual(url, '/interaction/learningintentiondetail/1/status/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'ajax_learningintentiondetail_status')
        self.assertEqual(resolver.kwargs,
            {'lid_id': '1'})

    def test_userlearningintentiondetail_cycle(self):
        url = reverse('userlearningintentiondetail_cycle', args=[1])
        self.assertEqual(url, '/interaction/learningintentiondetail/1/cycle/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'userlearningintentiondetail_cycle')
        self.assertEqual(resolver.kwargs,
            {'lid_id': '1'})

    def test_userlearningintentiondetail_progress_bar(self):
        url = reverse('userlearningintention_progress_bar', args=[1])
        self.assertEqual(url, '/interaction/learningintentiondetail/1/progress/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'userlearningintention_progress_bar')
        self.assertEqual(resolver.kwargs,
            {'lid_id': '1'})
