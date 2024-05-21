from django.contrib import admin
from django.utils.html import format_html

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
carts,\
cart_items,\
order_details,\
order_items,\
payment_details,\
library_images,\
motorbike_specs,\
motorbike_features,\
motorbike_feature_images



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


# Register your models here.
# admin.site.register(test_table)
admin.site.register(motor_types)
admin.site.register(brands, ImageBrandAdmin)
admin.site.register(motorbikes, DefaultImageAdmin)
# admin.site.register(motorbikes)
admin.site.register(motorbike_attributes, MotobikeAttributeAdmin)
admin.site.register(motorbike_skus, SkuImageAdmin)
admin.site.register(users)
admin.site.register(carts)
admin.site.register(cart_items)
admin.site.register(order_details)
admin.site.register(order_items)
admin.site.register(payment_details)
# admin.site.register(image_table_test, ImageTestAdmin)
admin.site.register(library_images, LibraryImageAdmin)
admin.site.register(motorbike_specs)
admin.site.register(motorbike_features)
admin.site.register(motorbike_feature_images, MotorbikeFeatureDetailImageAdmin)

