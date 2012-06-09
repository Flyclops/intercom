from django.test import TestCase
from . import models

class MembershipTypeModelTest (TestCase):

    def setUp(self):
        models.MembershipType.objects.all().delete()

    def test_creates_slug_from_name(self):
        mt = models.MembershipType(name='Hello, World!')
        mt.save()
        self.assertEqual(mt.slug, 'hello-world')
