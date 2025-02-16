from django.contrib import admin
from django.utils.html import format_html
from .models import Order, Product, Discount, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'price')
    search_fields = ('sku',)
    ordering = ('sku',)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'percentage')
    search_fields = ('code',)
    ordering = ('code',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('sku', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'get_username', 'get_total_items', 'get_subtotal', 'get_discount_amount', 'get_total', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'discount')
    search_fields = ('order_id', 'user__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'user', 'status', 'discount')
        }),
        ('Summary', {
            'fields': ('get_subtotal_display', 'get_discount_amount_display', 'get_total_display'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('get_subtotal_display', 'get_discount_amount_display', 'get_total_display')

    def get_username(self, obj):
        return obj.user.username if obj.user else '-'
    get_username.short_description = 'Customer'

    def get_total_items(self, obj):
        return obj.items.count()
    get_total_items.short_description = 'Total Items'

    def get_discount(self, obj):
        return f"{obj.discount.percentage}%" if obj.discount else '-'
    get_discount.short_description = 'Discount'

    def get_subtotal(self, obj):
        summary = obj.get_summary()
        return summary['subtotal']

    def get_discount_amount(self, obj):
        summary = obj.get_summary()
        return summary['discount_amount']

    def get_total(self, obj):
        summary = obj.get_summary()
        return summary['total']

    def get_subtotal_display(self, obj):
        return format_html('<b>{}</b>', self.get_subtotal(obj))
    get_subtotal_display.short_description = 'Subtotal'

    def get_discount_amount_display(self, obj):
        return format_html('<b>{}</b>', self.get_discount_amount(obj))
    get_discount_amount_display.short_description = 'Discount Amount'

    def get_total_display(self, obj):
        return format_html('<b>{}</b>', self.get_total(obj))
    get_total_display.short_description = 'Total'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'sku', 'quantity')
    list_filter = ('order',)
    search_fields = ('order__order_id', 'sku')
    ordering = ('-order__created_at', 'sku')