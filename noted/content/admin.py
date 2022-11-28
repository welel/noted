from django.contrib import admin

from content.models import Source, Note


admin.site.register(Source, admin.ModelAdmin)
admin.site.register(Note, admin.ModelAdmin)
