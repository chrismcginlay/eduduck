#core/test_eduduck_exceptions.py

from django.test import TestCase
from ..eduduck_exceptions import CheckRepError

class EduDuckExceptionTests(TestCase):

    def test_CheckRepError_inherits_from_Exception(self):
        self.assertIn(CheckRepError, Exception.__subclasses__())

    def test_CheckRepError_raises(self):
        self.fail("Write") 
