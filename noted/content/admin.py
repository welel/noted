from django.contrib import admin

from .models import Note, Source


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "draft", "anonymous", "created")
    list_filter = ("draft", "anonymous", "pin", "created", "modified", "lang")
    search_fields = ("title", "body_raw", "summary")
    raw_id_fields = ("author", "source", "fork")
    date_hierarchy = "created"
    list_editable = ("draft", "anonymous")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "link")
    list_filter = ("type",)
    search_fields = ("title", "description")
    list_editable = ("type",)
