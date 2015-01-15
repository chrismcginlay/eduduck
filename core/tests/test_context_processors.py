#core/tests/test_context_processors.py

from django.test import TestCase
from ..context_processors import git_most_recent_tag

class ContextProcessorsTests(TestCase):
    
    def setUp(self):
        pass
 
    def test_git_most_recent_tag(self):
        """Require git describe tag like mvp_0.1.0_rimmer-456-g22b45fc3"""
        mr_t = git_most_recent_tag(self.client.request)
        tag_regexp = "^[a-zA-Z]{3}_([0-9][.])+[0-9]"\
            "((_[a-z]+-[0-9]+-g[0-9a-fA-F]{7})|$)"
        self.assertGreater(len(mr_t), 10, "Tag seems to short")
        self.assertRegexpMatches(mr_t, tag_regexp, "Tag looks wrong")
            
