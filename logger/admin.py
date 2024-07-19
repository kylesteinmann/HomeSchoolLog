from django.contrib import admin
from .models import RequiredSubjects, Subject

class RequiredSubjectsAdmin(admin.ModelAdmin):
    list_display = ('state', 'name', 'type')
    search_fields = ('state', 'name', 'type')
    list_filter = ('state', 'name')

admin.site.register(RequiredSubjects, RequiredSubjectsAdmin)

class SubjectsAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'name', 'type')
    search_fields = ( 'user','name', 'type')
    list_filter = ( 'name', 'type')

admin.site.register(Subject, SubjectsAdmin)