import random
import re
from django.utils import timezone
from django.db import models


class MembershipType (models.Model):
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, blank=True, primary_key=True, 
                            help_text=("You can just leave this blank; "
                                       "it'll get filled in with something "
                                       "sensible based on the name of the "
                                       "membership type."))
    # rules (TimeRule, backref)

    def save(self, *args, **kwargs):
        if not self.slug:
            no_special_chars = re.sub('[^A-Za-z0-9 ]', '', self.name)
            self.slug = no_special_chars.replace(' ', '-').lower()
        return super(MembershipType, self).save(*args, **kwargs)

    def __unicode__(self):
        return (self.name + " membership")


class TimeRule (models.Model):
    DAY_CHOICES = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
        ('mf', 'Monday-Friday'),
        ('ss', 'Saturday/Sunday'),
        ('*', 'Every Day'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    is_open = models.BooleanField(default=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    membership = models.ForeignKey(MembershipType, related_name='rules')
    priority = models.IntegerField(help_text='Drag to reorder')

    def save(self, *args, **kwargs):
        if self.priority is None:
            try:
                last = self.membership.rules.all().order_by('-priority')[0]
                self.priority = last.priority + 1
            except IndexError:
                self.priority = 0

        return super(TimeRule, self).save(*args, **kwargs)

    class Meta:
        ordering = ('priority',)

    def __unicode__(self):
        days = dict(self.DAY_CHOICES)
        val = ('Open ' if self.is_open else 'Closed ') + days[self.day]
        if self.is_open:
            if self.opening_time:
                val += ' from ' + self.opening_time.strftime('%I:%M %p')
            if self.closing_time:
                val += ' until ' + self.closing_time.strftime('%I:%M %p')
        return val

    def day_matches(self, dt):
        w = dt.weekday()
        return (self.day == '*' or
                str(w) == self.day or
                (w < 5 and self.day == 'mf') or
                (w >= 5 and self.day == 'ss'))

    def applies(self, to_datetime):
        """
        Retrns true if this rule says that indyhall is open at the given
        datetime, false if it says that it's closed.  A None-value signifies
        nothing.
        """
        if self.day_matches(to_datetime):
            tz = timezone.get_current_timezone()
            current_time = to_datetime.astimezone(tz).time()

            if self.opening_time and current_time < self.opening_time:
                return
            if self.closing_time and current_time > self.closing_time:
                return

            return self.is_open


def unused_member_code():
    found_unused_code = False

    while not found_unused_code:
        code = random.randint(0, 999999)
        try:
            Member.objects.values('code').get(code=code)
        except Member.DoesNotExist:
            found_unused_code = True

    return str(code).zfill(6)


class Member (models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=256, help_text="The member's full name.")
    """The member's full name"""

    membership = models.ForeignKey(MembershipType)
    """The membership type for the member"""

    code = models.CharField(max_length=32, unique=True, default=unused_member_code,
                            help_text=("This should be a numeric code.  The "
                                       "default is an arbitrarily-generated "
                                       "unused code."))
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

    active = models.BooleanField(default=True)
    """Is the user active.  If they're deactivated, they won't be let in."""

    tone = models.CharField(max_length=1024, null=True, blank=True, 
                            help_text=("Use this to set a custom noise when "
                                       "the user enters a correct pass code.  "
                                       "Just leave it blank to use the "
                                       "default."))
    """The URL of the tone that will play upon member authentication"""

    last_access = models.DateTimeField(blank=True, default=timezone.now)
    """The time that the member last authenticated"""

    def access(self, commit=True):
        entry = AccessLogEntry()
        self.access_log.add(entry)
        entry.save()

        self.last_access = entry.access_datetime
        self.save()

    def is_allowed_access(self, at_datetime):
        """
        Return the allowance of the first non-None access rule for the given
        date and time.
        """
        for rule in self.membership.rules.all():
            allowance = rule.applies(at_datetime)
            if allowance is not None:
                return allowance

    def __unicode__(self):
        return (self.membership.name + " member " + self.name)


class AccessLogEntry (models.Model):
    member = models.ForeignKey(Member, related_name='access_log')
    access_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        tz = timezone.get_current_timezone()
        current_dt = self.access_datetime.astimezone(tz)
        return current_dt.strftime("%A, %d. %B %Y %I:%M%p")
