import pytz
from django.test import TestCase
from django.utils import timezone
from . import models

class MembershipTypeModelTest (TestCase):

    def setUp(self):
        models.MembershipType.objects.all().delete()

    def test_creates_slug_from_name(self):
        mt = models.MembershipType(name='Hello, World!')
        mt.save()
        self.assertEqual(mt.slug, 'hello-world')


class MemberModelTest (TestCase):

    def setUp(self):
        models.Member.objects.all().delete()
        models.MembershipType.objects.all().delete()

    def test_access_updates_last_accessed_time(self):
        mt = models.MembershipType.objects.create(name='Basic')
        m = models.Member(name='Mjumbe Poe', membership=mt, last_access=timezone.datetime(1, 1, 1, 0, 0, 0, 0, pytz.utc))
        m.save()

        time_now = timezone.now()
        self.assertLess(m.last_access, time_now)

        m.access()

        m = models.Member.objects.get(name='Mjumbe Poe')
        self.assertGreaterEqual(m.last_access, time_now)
