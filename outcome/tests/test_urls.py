#learning_intention/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):

    def test_learning_intention_view(self):
        url = reverse(
            'learning_intention', 
            kwargs={'lesson_id':1,'learning_intention_id': 2}
        )
        self.assertEqual(url, '/lesson/1/lint/2/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'learning_intention')
        self.assertEqual(resolver.kwargs, {
            'lesson_id': '1',
            'learning_intention_id': '2'
        })

    def test_learning_intention_edit(self):
        url = reverse(
            'lint_edit', kwargs={'lesson_id':1,'learning_intention_id':2})
        self.assertEqual(url, '/lesson/1/lint/2/edit/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'lint_edit')
        self.assertEqual(resolver.kwargs, {
            'lesson_id': '1',
            'learning_intention_id': '2'
        })
