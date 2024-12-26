from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryIconForm


admin.site.register(ProductImage)
admin.site.register(Model)
admin.site.register(Spec)
admin.site.register(SpecValue)
admin.site.register(Series)
admin.site.register(Profile)
admin.site.register(FavoriteProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(ShippingAddress)
admin.site.register(Region)
admin.site.register(City)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_icon', 'parent')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ['title']}
    form = CategoryIconForm

    def get_icon(self, obj):
        """Отображение иконки категорий"""
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width="30">')
            except:
                return '-'

        else:
            return '-'

    get_icon.short_description = 'Иконка'


class SpecInline(admin.TabularInline):
    model = SpecValue
    extra = 9


class ImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SpecInline, ImageInline]

    list_display = ('id', 'title', 'price', 'color_name', 'quantity', 'category', 'model', 'series', 'discount','get_photo')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ['title']}

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="60"')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Фото товара'


