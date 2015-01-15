#core/tests/test_context_processors.py

from django.test import TestCase
from ..context_processors import (
    git_most_recent_tag,
    git_most_recent_deployed
)

class ContextProcessorsTests(TestCase):
    
    def setUp(self):
        pass
 
    def test_git_most_recent_tag(self):
        """Require git describe tag like mvp_0.1.0_rimmer-456-g22b45fc3"""
        context_var = git_most_recent_tag(self.client.request)
        mr_t = context_var['MOST_RECENT_TAG']
        tag_regexp = "^[a-zA-Z]{3}_([0-9][.])+[0-9]"\
            "((_[a-z]+-[0-9]+-g[0-9a-fA-F]{7})|$)"
        self.assertGreater(len(mr_t), 9, "Tag seems too short")
        self.assertRegexpMatches(mr_t, tag_regexp, "Tag looks wrong")
           
    def test_git_most_recent_deployed(self):
        """Require git describe like DEPLOYED-2014-08-23/2028-147-gf4bf722"""
        context_var = git_most_recent_deployed(self.client.request)
        mr_d = context_var['MOST_RECENT_DEPLOYED']
        tag_regexp = "^DEPLOYED-20[0-9]{2}-[0-9]{2}-[0-9]{2}/[0-9]{4}((-[0-9]+-g[0-9a-zA-Z]{7})|$)"
        self.assertGreater(len(mr_d), 24, "Tag seem too short")
        self.assertRegexpMatches(mr_d, tag_regexp, "Tag looks wrong")
