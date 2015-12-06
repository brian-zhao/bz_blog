from django.test import TestCase
from blog.models import Blog

class SimpleTest(TestCase):
    def setUp(self):
        Blog(body='This is a test').save()

    def test_setup(self):
        self.assertEqual(1, len(Blog.objects.all()))
        self.assertEqual('This is a test', Blog.objects.all()[0].body)
