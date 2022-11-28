from django.contrib import admin

from content.models import SourceType, Source, Note


admin.site.register(SourceType, admin.ModelAdmin)
admin.site.register(Source, admin.ModelAdmin)
admin.site.register(Note, admin.ModelAdmin)
