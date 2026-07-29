from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import WorkEntry


class StaticViewSitemap(Sitemap):
    """Sitemap entries for the fixed, non-model-backed pages."""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["core:home", "core:about", "core:resources", "core:sunshine", "core:work_list", "core:contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Home page gets top priority; everything else shares 0.7.
        return 1.0 if item == "core:home" else 0.7


class WorkEntrySitemap(Sitemap):
    """Sitemap entries for each published work/timeline entry."""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return WorkEntry.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
