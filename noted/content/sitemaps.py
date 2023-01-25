from django.contrib.sitemaps import Sitemap

from .models import Note, Source


class NoteSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"
    i18n = True

    def items(self):
        return Note.objects.public()

    def lastmod(self, obj):
        return obj.modified


class SourceSitemap(Sitemap):
    changefreq = "never"
    priority = 0.6
    protocol = "https"
    i18n = True

    def items(self):
        return Source.objects.all()
