from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils.html import ma
from django.utils.html import escape
from django.utils.text import slugify

# def year_choices():
#     return [(r,r) for r in range(1984, datetime.today().year+1)]

# def current_year():
#     return datetime.today().year

# Create your models here.

# test table
# class test_table(models.Model):
#     item_id = models.AutoField(primary_key=True)
#     type_name = models.CharField(max_length=50, unique=True, null=True)

#     class Meta:
#         verbose_name_plural = 'test_table'


# 1st table: motor_types
class motor_types(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True, null=False, verbose_name='Kiểu xe')

    def __str__(self) -> str:
        return f"{self.type_name}"

    class Meta:
        verbose_name_plural = 'motor_types'
        #table name in database
        db_table = 'motor_types'



# 2nd table: brands
class brands(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=50, unique=True, null=False, verbose_name='Tên thương hiệu')
    brand_image = models.FileField(upload_to='brand_images', null=True)
    brand_order = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.brand_name}"

    class Meta:
        verbose_name_plural = 'brands'
        db_table = 'brands'

# 3rd table: motorbikes
class motorbikes(models.Model):
    motorbike_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=100, unique=True, null=False)
    description = models.CharField(max_length=2000, null=True, verbose_name='Mô tả')
    type = models.ForeignKey(motor_types, on_delete=models.CASCADE, null=True, verbose_name='Kiểu xe')
    brand = models.ForeignKey(brands, on_delete=models.CASCADE, null=True, verbose_name='Thương hiệu')
    image = models.ImageField(upload_to='default_images', null=True)
    banner_image = models.ImageField(upload_to='banner_images', null=True)
    motor_cost =  models.IntegerField(null=True)
    model_slug = models.SlugField(default="", null=True, blank=True, db_index=True,
                                #   editable=False
                                  )

    def __str__(self) -> str:
        return f"{self.model}"

    class Meta:
        verbose_name_plural = 'motorbikes'
        db_table = 'motorbikes'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.model)
        super().save(*args, **kwargs)

# 4th table: motorbike_attributes
class motorbike_attributes(models.Model):
    class Attribute_Type(models.TextChoices):
        COLOR = 'color'
        OPTION = 'option'

    attribute_id = models.AutoField(primary_key=True)

    attribute_type = models.CharField(
        max_length=10,
        choices=Attribute_Type.choices,
        default=Attribute_Type.COLOR,
        verbose_name='Kiểu phân loại')

    color_1 = models.CharField(max_length=10, blank=True, verbose_name='Màu sắc 1 - màu chính')
    color_2 = models.CharField(max_length=10, blank=True, verbose_name='Màu sắc 2 - màu phụ 1')
    color_3 = models.CharField(max_length=10, blank=True, verbose_name='Màu sắc 3 - màu phụ 2')



    value = models.CharField(max_length=50, null=False, verbose_name='Giá trị')

    def __str__(self) -> str:
        return f"{self.attribute_id} - {self.value} - {self.attribute_type}"

    class Meta:
        verbose_name_plural = 'motorbike_attributes'
        db_table = 'motorbike_attributes'

# 5th table: motorbike_skus
class motorbike_skus(models.Model):
    sku_id = models.AutoField(primary_key=True)
    # year = models.IntegerField(choices=year_choices, default=current_year)
    motorbike = models.ForeignKey(motorbikes, on_delete=models.CASCADE, null=True, verbose_name='Model xe')
    year = models.IntegerField(
        validators=[
            MinValueValidator(1984),
            MaxValueValidator(datetime.today().year + 1)
        ],
        verbose_name='Năm sản xuất',
        default=2024,
    )
    price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Giá')
    # image field
    color = models.ForeignKey(motorbike_attributes, related_name='color',
                              on_delete=models.CASCADE, null=True,
                              limit_choices_to= {'attribute_type': 'color'},
                              verbose_name='Phiên bản màu')
    option = models.ForeignKey(motorbike_attributes, related_name='option',
                               on_delete=models.CASCADE, null=True,
                               limit_choices_to={'attribute_type': 'option'},
                               verbose_name='Cấu hình')
    sku_image = models.ImageField(upload_to='sku_images', null=True)

    def __str__(self) -> str:
        return f"{self.motorbike.model} - {self.color} - {self.option} - {self.price}"

    class Meta:
        verbose_name_plural = 'motorbike_skus'
        db_table = 'motorbike_skus'

# 6th table: users
class users(models.Model):
    user_id = models.AutoField(primary_key=True)

    # phone = models.DecimalField(max_digits=15, decimal_places=0,
    #                             # blank=False, null=False,
    #                             blank=True, null=True,
    #                             # unique=True,
    #                             verbose_name='Số điện thoại',
    #                             )

    phone = models.CharField(
                            max_length=20,
                            # max_digits=15, decimal_places=0,
                            # blank=False, null=False,
                            blank=True, null=True,
                            # unique=True,
                            verbose_name='Số điện thoại',
                            )

    password = models.CharField(max_length=50,
                                null=True, blank=True,
                                # null=False, blank=False
                                )

    # password = models.
    full_name = models.CharField(max_length=100,
                                #  blank=False, null=False,
                                blank=True, null=True,
                                verbose_name='Họ và tên đầy đủ',
                                )

    address = models.CharField(max_length=500,
                            #    blank=False, null=False,
                               blank=True, null=True,
                               verbose_name='Địa chỉ',)

    email = models.EmailField(
                                # blank=False, null=False,
                                blank=True, null=True,
                                unique=True,
                                verbose_name='Email',
                                )

    def __str__(self) -> str:
        return f"{self.full_name} - {self.phone}"

    class Meta:
        verbose_name_plural = 'users'
        db_table = 'users'

# 7th table: carts
# class carts(models.Model):
#     cart_id = models.AutoField(primary_key=True)
#     total = models.IntegerField(null=True, verbose_name='Tổng số lượng xe')
#     user = models.ForeignKey(users, on_delete=models.CASCADE, null=True, verbose_name='Người mua')

#     def __str__(self) -> str:
#             return f"{self.user.full_name}"
#     class Meta:
#         verbose_name_plural = 'carts'
#         db_table = 'carts'



# 8th table: cart_items
class cart_items(models.Model):
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(users, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Người mua")
    quantity = models.IntegerField(null=True, verbose_name='Số lượng')

    # cart = models.ForeignKey(carts, on_delete=models.CASCADE, null=True)
    sku = models.ForeignKey(motorbike_skus, on_delete=models.CASCADE, null=True, verbose_name='Phiên bản')

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.sku.motorbike.model} - {self.sku.option} {self.sku.color} - {self.sku.price}, quantity: {self.quantity}"

    class Meta:
        verbose_name_plural = 'cart_items'
        db_table = 'cart_items'

# 9th table: order_details
class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    # status = models.CharField(max_length=50, null=True) #change to options

    created_date = models.DateField(null=True, blank=True, verbose_name='Ngày tạo đơn hàng')
    updated_on = models.DateField(null=True, blank=True, verbose_name='Ngày cập nhật đơn hàng')

    class Order_Status(models.TextChoices):
        ORDERED = 'ordered', 'Đã đặt hàng'
        PROCESSING = 'processing', 'Đang xử lý'
        SUCCESS = 'success', 'Giao hàng thành công'
        CANCELED = 'canceled', 'Đã hủy'

    order_status = models.CharField(
        max_length=20,
        choices=Order_Status.choices,
        default=Order_Status.ORDERED,
        verbose_name='Tình trạng',
        null=True,
        blank=True)

    total = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(users, on_delete=models.CASCADE, null=True, verbose_name='Người mua')

    address = models.CharField(max_length=500,
                            #    blank=False, null=False,
                               blank=True, null=True,
                               verbose_name='Địa chỉ giao hàng',)

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name_plural = 'orders'
        db_table = 'orders'

# 10th table: order_items
class order_items(models.Model):
    item_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(null=True, verbose_name='Số lượng')

    order = models.ForeignKey(orders, on_delete=models.CASCADE, null=True)
    sku = models.ForeignKey(motorbike_skus, on_delete=models.CASCADE, null=True, verbose_name='Phiên bản xe')

    def __str__(self) -> str:
        return f"{self.sku.motorbike.model} - {self.sku.option} {self.sku.color} - {self.sku.price}, quantity: {self.quantity}"

    class Meta:
        verbose_name_plural = 'order_items'
        db_table = 'order_items'


# test table for image
# class image_table_test(models.Model):
#     image_id = models.AutoField(primary_key=True)
#     image = models.ImageField()

#     # def image_tag(self):
#     #     return u'<img src="%s" />' % escape(self.image.path)
#     # image_tag.short_description = 'Image'
#     # image_tag.allow_tags = True

#12th table: library_images
class library_images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='library_images', verbose_name='Hình ảnh')

    motorbike = models.ForeignKey(motorbikes, on_delete=models.CASCADE, null=True, verbose_name='Model xe')

    def __str__(self) -> str:
        return f"{self.motorbike.model} - {self.image_id}"

    class Meta:
        verbose_name_plural = 'library_images'
        db_table = 'library_images'

#13th table: motorbike_specs
class motorbike_specs(models.Model):
    spec_id                     = models.AutoField(primary_key=True)
    motorbike = models.ForeignKey(motorbikes, unique=True, on_delete=models.CASCADE, null=True, verbose_name='Model xe')

    mass_ifself                 = models.TextField(verbose_name='Khối lượng bản thân', blank=True)
    length_width_height         = models.TextField(verbose_name='Dài x Rộng x Cao', blank=True)
    # width                       = models.IntegerField(verbose_name='Rộng', blank=True)
    # height                      = models.IntegerField(verbose_name='Cao', blank=True)

    wheel_hub_spacing           = models.TextField(max_length = 100 ,verbose_name='Khoảng cách trục bánh xe', blank=True)
    saddle_height               = models.TextField(max_length = 100 ,verbose_name='Độ cao yên', blank=True)
    ground_clearance            = models.TextField(max_length = 100 ,verbose_name='Khoảng sáng gầm xe', blank=True)
    fuel_tank_capacity          = models.TextField(max_length = 100 ,verbose_name='Dung tích bình xăng', blank=True)
    layer_sizes                 = models.TextField(max_length = 100, verbose_name='Kích cỡ lốp trước/sau', blank=True)
    front_fork                  = models.TextField(max_length = 100, verbose_name='Phuộc trước', blank=True)
    rear_fork                   = models.TextField(max_length = 100, verbose_name='Phuộc sau', blank=True)
    engine_type                 = models.TextField(max_length = 100, verbose_name='Loại động cơ', blank=True)
    max_power                   = models.TextField(max_length = 100, verbose_name='Công suất tối đa', blank=True)
    machine_viscosity_capacity  = models.TextField(max_length = 100, verbose_name='Dung tích nhớt máy', blank=True)
    fuel_consumption            = models.TextField(max_length = 100, verbose_name='Mức tiêu thụ nhiên liệu', blank=True)
    gearbox                     = models.TextField(max_length = 100, verbose_name='Hộp số', blank=True)
    drive_type                  = models.TextField(max_length = 100, verbose_name='Loại truyền động', blank=True)
    start_up_system             = models.TextField(max_length = 100, verbose_name='Hệ thống khởi động', blank=True)
    max_moment                  = models.TextField(max_length = 100, verbose_name='Mô-men xoắn cực đại', blank=True)
    cylinder_capacity           = models.TextField(max_length = 100, verbose_name='Dung tích xi lanh', blank=True)
    diameter_plunger_stroke     = models.TextField(max_length = 100, verbose_name='Đường kính x Hành trình pít tông', blank=True)
    compression_ratio           = models.TextField(max_length = 100, verbose_name='Tỷ số nén', blank=True)


    def __str__(self):
        return f"{self.motorbike.model}"

    class Meta:
        verbose_name_plural = 'motorbike_specs'
        db_table = 'motorbike_specs'


#14th table: motorbike_features
class motorbike_features(models.Model):
    feature_id = models.AutoField(primary_key=True)
    feature_type = models.CharField(max_length = 100, verbose_name='Kiểu tính năng')
    feature_description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.feature_type} - {self.feature_description}"

    class Meta:
        verbose_name_plural = 'motorbike_features'
        db_table = 'motorbike_features'

#15th table: motorbike_feature_images
class motorbike_feature_images(models.Model):
    image_id = models.AutoField(primary_key=True)
    feature = models.ForeignKey(motorbike_features, on_delete=models.CASCADE, null=True, verbose_name='Kiểu tính năng')
    motorbike = models.ForeignKey(motorbikes, on_delete=models.CASCADE, null=True, verbose_name='Model xe')
    image = models.ImageField(upload_to='feature_images', verbose_name='Hình ảnh')
    description = models.CharField(max_length=200, blank=True, verbose_name='Mô tả')

    def __str__(self) -> str:
        return f"{self.motorbike.model} - {self.image_id}"

    class Meta:
        verbose_name_plural = 'motorbike_feature_images'
        db_table = 'motorbike_feature_images'
