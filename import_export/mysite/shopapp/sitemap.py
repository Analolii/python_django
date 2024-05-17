from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product
from .models import Order


class ShopSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.3

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_at




