from django.contrib import admin
from .models import (
    GameCategory,
    Product,
    Comments,
    ImageGallery,
    Orders,
    OrderItem
)


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'created', 'paid']
    list_filter = ['created', 'paid']
    inlines = [OrderItemAdmin]  # Здесь должен быть класс, а не модель


admin.site.register([
    ImageGallery
])


@admin.register(GameCategory)
class AdminGameCategory(admin.ModelAdmin):
    fields = ['slug', 'name']
    prepopulated_fields = {'slug': ('name',)}


class ImageGalleryInline(admin.StackedInline):
    model = ImageGallery


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    fields = ['title', 'slug', 'category', 'region', 'desc', 'availability', 'overview', 'available', 'price',
              'salesman']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageGalleryInline]


@admin.register(Comments)
class AdminComments(admin.ModelAdmin):
    fields = ['image', 'name', 'text', 'active']
