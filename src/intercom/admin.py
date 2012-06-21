from django.contrib import admin
from django.db.models import Count, Max
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

class AccessLogEntryInline (admin.TabularInline):
    model = models.AccessLogEntry
    extra = 0
    ordering = ['-access_datetime']
    readonly_fields = ['access_datetime']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

class MemberAdmin (admin.ModelAdmin):
    inlines = [AccessLogEntryInline]

    readonly_fields = ['last_access']
    list_display = ['name', 'membership', 'last_access', 'num_accesses']
    list_display_links = ['name']
    list_editable = []
    list_filter = ['membership']
    list_select_related = True
    ordering = ['-last_access']
    search_fields = ['name']

    def queryset(self, request):
        qs = super(MemberAdmin, self).queryset(request)
        qs = qs.annotate(num_accesses=Count('access_log'))
        return qs

    def num_accesses(self, obj):
        return obj.num_accesses
    num_accesses.short_description = 'Access Count'
    num_accesses.admin_order_field = 'num_accesses'

admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.MembershipType, MembershipTypeAdmin)
