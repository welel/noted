from django.contrib import admin

from actions.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("user", "verb", "target", "created")
    list_filter = ("created", "verb", "target_ct")
    search_fields = ("verb",)
