from django.contrib import admin
from .models import RequiredSubjects

class RequiredSubjectsAdmin(admin.ModelAdmin):
    list_display = ('state', 'name', 'type')
    search_fields = ('state', 'name', 'type')
    list_filter = ('state', 'name')

admin.site.register(RequiredSubjects, RequiredSubjectsAdmin)