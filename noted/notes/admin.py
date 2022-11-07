from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from notes.models import Note, Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'private', 'anonymous',
                    'datetime_created', 'datetime_modified')
    search_fields = ('title', 'body_raw', )
    list_editable = ('private', 'anonymous')
    ordering = ('-datetime_created',)
    date_hierarchy = 'datetime_created'


admin.site.register(Comment, MPTTModelAdmin)
