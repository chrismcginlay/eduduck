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
        self.assertGreater(len(mr_t), 9, "Tag seems too short")
        self.assertRegexpMatches(mr_t, tag_regexp, "Tag looks wrong")
           
    def test_git_most_recent_deployed(self):
        """Require git describe like DEPLOYED-2014-08-23/2028-147-gf4bf722"""
        mr_d = git_most_recent_deployed(self.client.request)
        tag_regext = "^DEPLOYED-20[0-9]{2}-[0-9]{2}-[0-9]{2}/[0-9]{4}-[0-9]+-g[0-9a-fA-F]$"
        self.assertGreater(len(mr_d), 24, "Tag seem too short")
        self.assertRegexpMatches(mr_d, tag_regexp, "Tag looks wrong")
