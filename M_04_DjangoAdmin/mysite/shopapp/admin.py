from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description='Archived')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchived')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'price', 'description', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'discount'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
          }),
        ('Price options', {
            'fields': ('price', 'discount'),
        }),
        ('Extra info', {
            'fields': ('archived',),
            'classes': ('collapse',),
        }),
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username



# Register your models here.
