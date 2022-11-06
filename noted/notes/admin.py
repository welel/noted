from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'private', 'anonymous', 'date')
    search_fields = ('title', 'body_raw', )
    list_editable = ('private', 'anonymous')
    ordering = ('-date',)
    date_hierarchy = 'date'
