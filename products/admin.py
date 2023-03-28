from django.contrib import admin

from products.models import Bag, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category')
    search_fields = ('name',)
    ordering = ('name',)


# we can use a TabularInline if there is a FOREIGN KEY link
class BagAdmin(admin.TabularInline):
    model = Bag
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    # in order not to display extra fields in the admin panel in the user's bag
    extra = 0
