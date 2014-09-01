# video/tests/test_utils.py

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..utils import get_youtube_id_from_url, validate_youtube_url

class VideoUtilTest(TestCase):

    def test_correct_id_returned_from_urls(self):
        """Various URL structures need testing"""

        # BTW, you *will* regret visiting any of these URLs
        urls_2_pass = [
            r"http://youtu.be/dQw4w9WgXcQ",
            r"http://www.youtube.com/embed/dQw4w9WgXcQ",
            r"http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            r"http://www.youtube.com/?v=dQw4w9WgXcQ",
            r"http://www.youtube.com/v/dQw4w9WgXcQ",
            r"http://www.youtube.com/e/dQw4w9WgXcQ",
            r"http://www.youtube.com/watch?feature=player_embedded&v=dQw4w9WgXcQ",
            r"http://www.youtube.com/?feature=player_embedded&v=dQw4w9WgXcQ",
        ]
        expected_id = "dQw4w9WgXcQ"

        for url in urls_2_pass:
            self.assertEqual(get_youtube_id_from_url(url), expected_id, url)

    def test_nonetype_returned_from_urls(self):
        """These are failure cases and should return None"""
        
        urls_2_fail = [
            r"http://yout.be/dQw49WgXc",
            r"http://youtu.be/dQw49WgXc",
            r"http://www.youtube.com/embed/dqW4w9", 
            r"http://www.youtube.com/v/dqW4w9", 
            r"http://www.youtube.com/watch?feature=player_embedded&v=dQw",
        ]
        for url in urls_2_fail:
            self.assertEqual(get_youtube_id_from_url(url), None)

    def test_validate_url(self):
        
        urls_2_fail = [
            r"http://yout.be/dQw49WgXc",
            r"http://youtu.be/dQw49WgXc",
            r"http://www.youtube.com/embed/dqW4w9", 
            r"http://www.youtube.com/v/dqW4w9", 
            r"http://www.youtube.com/watch?feature=player_embedded&v=dQw",
        ]
        for url in urls_2_fail:
            with self.assertRaises(ValidationError):
                validate_youtube_url(url)

        urls_2_pass = [
            r"http://youtu.be/dQw4w9WgXcQ",
            r"http://www.youtube.com/embed/dQw4w9WgXcQ",
            r"http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            r"http://www.youtube.com/?v=dQw4w9WgXcQ",
            r"http://www.youtube.com/v/dQw4w9WgXcQ",
            r"http://www.youtube.com/e/dQw4w9WgXcQ",
            r"http://www.youtube.com/watch?feature=player_embedded&v=dQw4w9WgXcQ",
            r"http://www.youtube.com/?feature=player_embedded&v=dQw4w9WgXcQ",
        ]
        for url in urls_2_pass:
            validate_youtube_url(url)


