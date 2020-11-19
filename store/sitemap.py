from django.contrib.sitemaps import Sitemap
from listelement.models import Element

class ElementSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Element.objects.filter(type=1)

    def lastmod(self, obj):
        return obj.updated