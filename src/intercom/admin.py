from django.contrib import admin
from . import models

class TimeRuleInline (admin.TabularInline):
    model = models.TimeRule
    extra = 0
    ordering = ['priority']

class MembershipTypeAdmin (admin.ModelAdmin):
    inlines = [TimeRuleInline]

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
            'js/admin-list-reorder.js',
        )

class MemberAdmin (admin.ModelAdmin):
    readonly_fields = ['last_access']
    list_display = ['name', 'membership', 'last_access']
    list_display_links = ['name']
    list_editable = []
    list_filter = ['membership']
    list_select_related = True
    ordering = ['-last_access']
    search_fields = ['name']

admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.MembershipType, MembershipTypeAdmin)
