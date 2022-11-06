from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from notes.models import Note, Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'private', 'anonymous', 'date')
    search_fields = ('title', 'body_raw', )
    list_editable = ('private', 'anonymous')
    ordering = ('-date',)
    date_hierarchy = 'date'


admin.site.register(Comment, MPTTModelAdmin)
