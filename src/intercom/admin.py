from django.contrib import admin
from . import models

class TimeRuleInline (admin.TabularInline):
    model = models.TimeRule
    extra = 0

class MembershipTypeAdmin (admin.ModelAdmin):
    inlines = [TimeRuleInline]

admin.site.register(models.Member)
admin.site.register(models.MembershipType, MembershipTypeAdmin)
