from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from notes.models import Note, Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'private', 'anonymous',
                    'datetime_created', 'datetime_modified', 'tag_list')
    search_fields = ('title', 'body_raw', )
    list_editable = ('private', 'anonymous')
    ordering = ('-datetime_created',)
    date_hierarchy = 'datetime_created'


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Comment, MPTTModelAdmin)
