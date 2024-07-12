from django.contrib import admin
from base.models import StateRequirements

class StateRequirementsAdmin(admin.ModelAdmin):
    list_display = ('state', 'core_hours', 'total_hours', 'year_start', 'year_end')
    search_fields = ('state',)
    list_filter = ('year_start', 'year_end')

admin.site.register(StateRequirements, StateRequirementsAdmin)