from django.test import TestCase
import os

# Create your tests here.
class Dirtest(TestCase):

    def test_something(self):
        print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.assertEquals(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.path.dirname(os.path.dirname(os.path.abspath(__file__))))