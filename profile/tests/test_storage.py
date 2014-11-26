#profile/tests/test_storage
from os import system
from os.path import isfile, join
from django.conf import settings
from django.test import TestCase

from ..storage import OverwriteFSStorage

class StorageTests(TestCase):

    def test_get_available_name_deletes_existing_file(self):
        """get_available_name can delete existing file"""
        
        fss = OverwriteFSStorage(
            base_url=settings.MEDIA_URL, 
            location=settings.MEDIA_ROOT,
        )
        #Put a file in the filesystem
        path = join(settings.MEDIA_ROOT, 'testjunk.txt')
        system("touch {0}".format(path))
        
        #see that the filename is still available for rewrite
        name_avail = fss.get_available_name(path)
        self.assertEqual(name_avail, path)
        
        assert(not(isfile(path)))
