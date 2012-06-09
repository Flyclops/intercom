import random
import re
from datetime import datetime
from django.db import models


class MembershipType (models.Model):
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, blank=True, primary_key=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            no_special_chars = re.sub('[^A-Za-z0-9 ]', '', self.name)
            self.slug = no_special_chars.replace(' ', '-').lower()
        return super(MembershipType, self).save(*args, **kwargs)

    def __unicode__(self):
        return (self.name + " membership")


def unused_member_code():
    found_unused_code = False

    while not found_unused_code:
        code = random.randint(0, 999999)
        try:
            Member.objects.get(code=code)
        except Member.DoesNotExist:
            found_unused_code = True

    return str(code).zfill(6)


class Member (models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=256)
    """The member's full name"""

    membership = models.ForeignKey(MembershipType)
    """The membership type for the member"""

    code = models.CharField(max_length=32, unique=True, default=unused_member_code)
    """The entry code for the user"""
    # NOTE: consider storing the code encrypted, like User.password.  There are
    #       a few ways this could be done.  We could store a common salt to
    #       calculate all hashes.  This would speed up comparisons (an entered
    #       code would only have to be hashed once; if each code had a random
    #       salt, the hash would have to be recalculated to compare against each
    #       code).  However, giving each code its own hash feels safer.
    #
    #       Down-sides to encrypting the code are primarily slower comparison
    #       times.
    #
    #       For now we will leave it unhashed.  We can always change our mind
    #       with a migration later.  Of course, it would be a one-way migration.

    tone = models.CharField(max_length=1024, null=True, blank=True)
    """The URL of the tone that will play upon member authentication"""

    last_access = models.DateTimeField(blank=True, default=datetime.now)
    """The time that the member last authenticated"""

    def __unicode__(self):
        return (self.membership.name + " member " + self.name)
