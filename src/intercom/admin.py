from django.contrib import admin
from . import models

class TimeRuleInline (admin.TabularInline):
    model = models.TimeRule
    extra = 0
    ordering = ['priority']

class MembershipTypeAdmin (admin.ModelAdmin):
    inlines = [TimeRuleInline]

class MemberAdmin (admin.ModelAdmin):
    readonly_fields = ['last_access']
    list_display = ['name', 'membership', 'last_access']
    list_display_links = ['name']
    list_editable = []
    list_filter = ['membership']
    search_fields = ['name']

admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.MembershipType, MembershipTypeAdmin)
