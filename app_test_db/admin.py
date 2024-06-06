from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, Textarea

# from .models import test_table,\
# motor_types,\
# brands,\
# motorbikes,\
# motorbike_attributes,\
# motorbike_skus,\
# users,\
# carts,\
# cart_items,\
# order_details,\
# order_items,\
# payment_details,\
# image_table_test,\
# library_images,\
# motorbike_specs,\
# motorbike_features,\
# motorbike_feature_images

from .models import motor_types,\
brands,\
motorbikes,\
motorbike_attributes,\
motorbike_skus,\
users,\
cart_items,\
order_items,\
library_images,\
motorbike_specs,\
motorbike_features,\
motorbike_feature_images,\
orders

# carts,\



# class ImageTestAdmin(admin.ModelAdmin):
#     def image_tag(self, obj):
#         return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

#     list_display = ['image_id', 'image_tag',]

class ImageBrandAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.brand_image.url))
        except:
            return format_html('<img src="" style="max-width:200px; max-height:200px"/>')

    list_display = ['brand_name', 'image_tag', ]


class DefaultImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        except:
            return format_html('<img src="" style="max-width:200px; max-height:200px"/>')

    def banner_image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-height:200px"/>'.format(obj.banner_image.url))
        except:
            return format_html('<img src="" style="max-height:200px"/>')

    list_display = ['model', 'image_tag', 'banner_image_tag']
    list_filter = ["brand"]

class SkuImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.sku_image.url))
        except:
            return format_html('<img src="" style="max-width:200px; max-height:200px"/>')

    list_display = ['sku_id', 'motorbike', 'color', 'option', 'price', 'image_tag', ]

class LibraryImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.sku_image.url))
        except:
            return format_html('<img src="" style="max-width:200px; max-height:200px"/>')

    list_display = ['image_id', 'image_tag',]

class MotobikeFeatureImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.sku_image.url))
        except:
            return format_html('<img src="" style="max-width:200px; max-height:200px"/>')

    list_display = ['motorbike', 'feature', 'image_tag', 'description']


class MotorbikeFeatureDetailImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
        except:
            return format_html('<img src="" style="max-width:200px; max-height:200px"/>')

    list_display = ['feature', 'motorbike', 'description', 'image_tag', ]
    list_filter = ['motorbike', 'feature']
    ordering = ['image_id']

class MotobikeAttributeAdmin(admin.ModelAdmin):
    list_filter = ["attribute_type"]

class MotorbikeSpecAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
    }

class OrderAdmin(admin.ModelAdmin):
    list_filter = ["created_date", "user", "order_status"]

class ReverseOrderFilter(admin.SimpleListFilter):
    title = 'Order'
    parameter_name = 'order'

    def lookups(self, request, model_admin):
        # Lấy danh sách các giá trị unique của trường 'order'
        queryset = model_admin.get_queryset(request)
        order_values = queryset.values_list('order', flat=True).distinct()

        # Đảo ngược danh sách giá trị
        # reversed_order_values = reversed(list(order_values))
        reversed_order_values = (list(order_values))

        # Trả về danh sách các lựa chọn
        return [(value, str(value)) for value in reversed_order_values]

    def queryset(self, request, queryset):
        # Áp dụng bộ lọc dựa trên giá trị được chọn
        if self.value():
            return queryset.filter(order=self.value())
        return queryset

class ReverseChoicesFieldListFilter(admin.ChoicesFieldListFilter):
    def choices(self, changelist):
        choices = list(super().choices(changelist))
        choices.reverse()
        return choices

class OrderItemAdmin(admin.ModelAdmin):
    ordering = ['-order']
    list_filter = (ReverseOrderFilter, )


# Register your models here.
# admin.site.register(test_table)
admin.site.register(motor_types)
admin.site.register(brands, ImageBrandAdmin)
admin.site.register(motorbikes, DefaultImageAdmin)
# admin.site.register(motorbikes)
admin.site.register(motorbike_attributes, MotobikeAttributeAdmin)
admin.site.register(motorbike_skus, SkuImageAdmin)
admin.site.register(users)
# admin.site.register(carts)
admin.site.register(cart_items)
admin.site.register(orders, OrderAdmin)
admin.site.register(order_items, OrderItemAdmin)
# admin.site.register(image_table_test, ImageTestAdmin)
admin.site.register(library_images, LibraryImageAdmin)
admin.site.register(motorbike_specs, MotorbikeSpecAdmin)
admin.site.register(motorbike_features)
admin.site.register(motorbike_feature_images, MotorbikeFeatureDetailImageAdmin)

