from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import UserForm
from .models import users, brands, motorbikes, motorbike_skus, motorbike_feature_images, motorbike_specs, cart_items, orders, order_items, motor_types
from django.http import HttpResponse, JsonResponse, FileResponse, StreamingHttpResponse
import json
from datetime import date
from django.conf import settings
from .pdf_engine import PDF, money_format
from fpdf import FPDF
from pathlib import Path
import os


# functions
def get_brands():
    return brands.objects.all().order_by('brand_order')

def get_motor_types():
    return motor_types.objects.all().order_by('type_id')

def get_current_user(request):
    user_id = request.session.get("user_id")
    user = None

    if (user_id):
        user = users.objects.get(user_id = user_id)

    return user


# Create your views here.
def login(request):
    if request.method == "POST":
        # form = UserForm(request.POST)
        # print(form['phone'].value())
        # return render(request, "login.html", {"form" : form})
        user_phone = request.POST.get('phone')
        user_password = request.POST.get('password')

        print("phone: ", user_phone)
        print("password: ", user_password)

        try:
            result = users.objects.get(phone = user_phone, password = user_password)
            request.session["user_id"] = str(result.user_id)
            print("Result: ", result)
            print(request.session.get("user_id"))
            return redirect("home")
        except:
            print("No user match")
            error = "Số điện thoại hoặc mật khẩu không đúng !"
            return render(request, "login.html", {
                "error": error,
            })
    else:
        # form = UserForm()
        # return render(request, "login.html", {"form" : form})
        return render(request, "login.html", {
            "error": "",
        })


def signup(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            new_user = users()
            new_user.phone = phone
            new_user.password = password
            new_user.full_name = full_name
            new_user.address = address
            new_user.email = email

            new_user.save()


        print("phone: ", phone)
        print("full name: ", full_name)
        print("address: ", address)
        print("email: ", email)
        print("password: ", password)
        print("confirm pasword: ",confirm_password)

        return redirect("login")


    else:
        return render(request, "registration.html")

def home(request):
    motor_brands = brands.objects.all().order_by('brand_order')
    motorbike_list = motorbikes.objects.all().order_by('motorbike_id')
    motorbike_types = motor_types.objects.all()
    home_skus = []
    default_skus = []
    count = 0

    user_id = request.session.get("user_id")
    user = None

    if (user_id):
        user = users.objects.get(user_id = user_id)

    # print(motorbike_list)
    for motor in motorbike_list:
        skus = motorbike_skus.objects.filter(motorbike = motor).order_by('price')
        default_skus.append(skus[0])
        internal_count = 0
        just_color = True

        results = (skus.values('option').order_by())

        unique_set = set(tuple(d.items()) for d in results)

        unique_dict = [dict(item) for item in unique_set]

        if ((len(unique_dict) > 1)):
            for sku in skus:
                if count == 0:
                    home_skus.append(sku)
                    count = count + 1
                else:
                    if (sku.motorbike != home_skus[count-1].motorbike):
                        home_skus.append(sku)
                        count = count + 1
                    else:
                        if (sku.option != (home_skus[count - 1].option) ):
                            if ((sku.color) != (home_skus[count - 1].color)):
                                home_skus.append(sku)
                                count = count + 1


    for motor in motorbike_list:
        # motor.save()
        skus = motorbike_skus.objects.filter(motorbike = motor).order_by('option')
        internal_count = 0
        just_color = True

        results = (skus.values('option').order_by())

        unique_set = set(tuple(d.items()) for d in results)

        unique_dict = [dict(item) for item in unique_set]

        if ((len(unique_dict) == 1)):
            for item in skus:
                home_skus.append(item)



    return render(request, "home.html", {
        'brands': motor_brands,
        'motorbikes': motorbike_list,
        'skus': home_skus,
        'default_option': default_skus,
        'user': user,
        'motorbike_types': motorbike_types,
        'brands_cat': motor_brands,
        'motorbike_types_cat': motorbike_types,
    })

def motor_detail(request, slug):
    motor = motorbikes.objects.get(model_slug = slug)
    motor_skus = motorbike_skus.objects.filter(motorbike = motor).order_by('price')

    option = []

    user_id = request.session.get("user_id")
    user = None

    if (user_id):
        user = users.objects.get(user_id = user_id)


    for sku in motor_skus:
        option.append(sku.option)

    option = list(set(option))

    motor_features = motorbike_feature_images.objects.filter(motorbike = motor).order_by('image_id')

    # fields = [field.value for field in motor_features[0]._meta.get_fields()]
    # try:
    #     field_names = [field.name for field in (motor_features[0])._meta.get_fields()]
    # except:
    #     pass
        # for field in field_names:
        # #     print(getattr( motor_features[0], field))
        #     print(getattr( (motor_features[0]), field), " ")

    # print(fields)

    # for field in fields:
    #     print(getattr( motor_features[0], field))

    motor_specs = motorbike_specs.objects.get(motorbike = motor)

    spec_fields = []

    motor_spec_list = {}

    new_line_str = "\r\n"

    html_br_str = "<br>"

    if motor_specs != None:
        spec_fields = [field.name for field in motor_specs._meta.get_fields()]

        print(spec_fields)

        try:
        # 'spec_id', 'motorbike'
            spec_fields.remove('spec_id')
            spec_fields.remove('motorbike')
        except:
            pass


        for spec in spec_fields:
            spec_value = str(getattr(motor_specs, spec))
            spec_field = str(motor_specs._meta.get_field(spec).verbose_name)

            if new_line_str in spec_value:
                spec_value = spec_value.replace(new_line_str, html_br_str)

            motor_spec_list[str(spec_field)] = spec_value

    return render(request, "product.html", {
        'motorbike': motor,
        'options': option,
        'skus': motor_skus,
        'motor_features': motor_features,
        'user': user,
        'motor_specs': motor_spec_list,
    })

def logout(request):
    request.session.flush()
    return redirect("home")

def add_to_cart(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)
        sku_id = data.get('sku_id')

    if sku_id == "":
        response_data = {'success': True, 'message': 'Vui lòng chọn phiên bản của phương tiện để thêm vào giỏ hàng!'}
    else:
        user_id = request.session.get("user_id")
        sku_id = int(sku_id)

        sku = motorbike_skus.objects.get(sku_id = sku_id)

        user = None

        if (user_id):
            user = users.objects.get(user_id = user_id)
            items = cart_items.objects.filter(user = user)
            duplicate = False

            for item in items:
                if item.sku == sku:
                    item.quantity = item.quantity + 1
                    item.save()
                    duplicate = True

            if duplicate != True:
                new_item = cart_items()
                new_item.user = user
                new_item.quantity = 1
                new_item.sku = sku
                new_item.save()

            response_data = {'success': True, 'message': 'Thêm sản phẩm vào giỏ hàng thành công!'}

        else:
            response_data = {'success': True, 'message': 'Vui lòng đăng nhập để có thể thêm sản phẩm vào giỏ hàng!'}

    return JsonResponse(response_data)

def cart(request):
    # print(str(settings.MEDIA_ROOT) + '''\logo\horizontal_logo.png''')


    if request.method == 'POST':
        user_id = request.session.get("user_id")
        user_id = int(user_id)

        current_user = users.objects.get(user_id = user_id)

        if current_user:
            items = cart_items.objects.filter(user = current_user)
            total_cast = 0
            # create new order
            new_order = orders()
            new_order.created_date = date.today()
            new_order.updated_on = date.today()
            new_order.order_status = orders.Order_Status.ORDERED
            new_order.user = current_user
            new_order.save()

            # create new item order
            for item in items:
                new_order_item = order_items()
                new_order_item.quantity = item.quantity
                new_order_item.order = new_order
                new_order_item.sku = item.sku
                new_order_item.save()

                total_cast += item.sku.price * item.quantity

                # item.delete()

            new_order.total = total_cast
            new_order.save()

            # create bill
            order_bill = PDF()
            order_bill.add_page()

            # Set auto page break
            order_bill.set_auto_page_break(auto=True, margin=15) # margin is the space from bttom of page to page break

            order_bill.add_centered_image(str(settings.MEDIA_ROOT) + '''\logo\horizontal_logo.png''')
            order_bill.ln(5)

            # order_bill.add_font('NunitoBold', '', r'Nunito-Bold.ttf')

            font_path = os.path.join(os.path.dirname(__file__), "Nunito-Bold.ttf")
            order_bill.add_font('NunitoBold', '', font_path)
            order_bill.set_font('NunitoBold', '', 20)

            order_bill.set_x(0)
            order_bill.cell(0, 10, 'HÓA ĐƠN BÁN HÀNG', 0, 1, 'C')
            order_bill.ln(5)

            order_bill.set_font('NunitoBold', '', 12)  # Thiết lập font chữ Arial cho nội dung bảng
            order_bill.set_x(15)
            order_bill.cell(80, 10, f'Khách hàng: {current_user.full_name}')

            order_bill.cell(40, 10)
            order_bill.cell(40, 10, f'SĐT: {current_user.phone}')
            order_bill.ln()

            order_bill.set_x(15)
            order_bill.cell(80, 10, f'Ngày lập hóa đơn: {new_order.created_date}')
            order_bill.ln()

            address = f"Địa chỉ: {new_order.address}"
            order_bill.set_x(15)
            order_bill.multi_cell(180, 10, address)

            # Dữ liệu cho bảng
            data = [
                ['STT', 'Phương tiện (Phiên bản và số lượng)', 'Đơn giá'],
                # ['1', 'SH160i, Đặc biệt ABC, Đen đỏ trắng, số lượng: 1', '101.000.000đ'],
                # ['1', 'SH160i, Đặc biệt ABC, Đen đỏ trắng, số lượng: 1', '101.000.000đ'],
                # ['1', 'SH160i, Đặc biệt ABC, Đen đỏ trắng, số lượng: 1', '101.000.000đ'],
            ]

            count = 1
            for item in items:
                new_data = [str(count), f'{item.sku.motorbike.model}, {item.sku.option.value}, {item.sku.color.value}, Số lượng: {item.quantity}', money_format(str(item.sku.price))]
                count = count + 1
                data.append(new_data)

                # will need to add item.delete() here
                item.delete()

            # Gọi phương thức create_table để vẽ bảng
            order_bill.create_table(data, money_format(str(total_cast)))
            order_bill.ln(15)

            order_bill.set_x(15)
            order_bill.cell(60, 10, 'Chữ ký bên mua', 0, 0, 'C')
            order_bill.cell(60, 10, '')
            order_bill.cell(60, 10, 'Chữ ký bên bán', 0, 0, 'C')

            order_bill.output(str(settings.MEDIA_ROOT) + f'\\order_bills\\{new_order.order_id}.pdf')

# app_test_db\static\fonts\Nunito\static\Nunito-Bold.ttf


            return redirect("order-list")
        else:
            return redirect("login")

    else:
        user_id = request.session.get("user_id")
        user = None
        items = None
        total = 0

        if (user_id):
            user = users.objects.get(user_id = user_id)
            items = cart_items.objects.filter(user = user, quantity__gt = 0)
            for item in items:
                total += item.sku.price * item.quantity
        else:
            return redirect("login")
            pass

        return render(request, "cart.html", {
            "user": user,
            "items": items,
            "total": total,
        })

def change_cart_item_quantity(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        user_id = int(request.session.get("user_id"))
        current_user = users.objects.get(user_id = user_id)
        cart_item = cart_items.objects.get(item_id = item_id)

        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        current_cart_items = cart_items.objects.filter(user = current_user)
        total_cast = 0

        if current_cart_items.count() > 0:
            for item in current_cart_items:
                total_cast += item.sku.price * item.quantity

    response_data = {'success': True, 'message': 'Thay đổi số lượng phương tiện thành công!', 'cast_value': str(total_cast)}

    return JsonResponse(response_data)

def order_list(request):
    user_id = request.session.get("user_id")
    user_id = int(user_id)

    current_user = users.objects.get(user_id = user_id)
    user_orders = orders.objects.filter(user = current_user).order_by('created_date', '-order_id')
    current_orders = {}

    for order in user_orders:
        try:
            order_item = (order_items.objects.filter(order = order))[0]
            current_orders[order] = order_item.sku
        except:
            pass

    print(current_orders)

    return render(request, "order-list.html", {
        'orders': current_orders,
    })

def order_detail(request, order_id):

    current_order = orders.objects.get(order_id = order_id)

    current_user_id = int(request.session.get("user_id"))

    if current_user_id:
        order_user_id = current_order.user.user_id

        if current_user_id == order_user_id:
            current_order_items = order_items.objects.filter(order = current_order)
            return render(request, "order-detail.html", {
                "order": current_order,
                "items": current_order_items,
            })
        else:
            return redirect("login")
    else:
        return redirect("login")

def order_bill_download(request, order_id):
    file_name = str(order_id) + '.pdf'
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'order_bills', file_name)
    file_name = 'order_bill_' + str(order_id) + '.pdf'
    print(pdf_path)

    # return redirect("home")

    if os.path.exists(pdf_path):
        response = StreamingHttpResponse(open(pdf_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
    return HttpResponse('PDF not found.')

def search_engine(request):
    user_id = request.session.get("user_id")
    user = None

    if (user_id):
        user = users.objects.get(user_id = user_id)

    print("test")
    input_str = request.POST['input']
    input_str = str(input_str)

    key_list = input_str.split()

    result_motor_list = []
    result_brand_list = []
    result_sku_list = []
    result_default_option = []

    motors = motorbikes.objects.all()

    for input in key_list:
        print('\n')
        input = input.lower()

        for motor in motors:
            model = str(motor.model).lower()
            if input in model:
                result_motor_list.append(motor)
                result_brand_list.append(motor.brand)

                tmp_skus = motorbike_skus.objects.filter(motorbike = motor)

                # result_sku_list.extend(list(tmp_skus))
                # result_default_option.append(tmp_skus[0])

    result_motor_list       = list(set(result_motor_list))

    for motor in result_motor_list:
        tmp_skus = motorbike_skus.objects.filter(motorbike = motor).order_by('price')
        options = []

        for sku in tmp_skus:
            options.append(sku.option)

        options = list(set((options)))

        if len(options) > 1:
            tmp_options = [tmp_skus[0].option]
            result_sku_list.append(tmp_skus[0])
            result_default_option.append(tmp_skus[0])
            count = 1

            for sku in tmp_skus:
                tmp_option = sku.option
                if tmp_option not in tmp_options:
                    tmp_options.append(sku.option)
                    tmp_sku = tmp_skus.filter(option = tmp_option)
                    for sku_1 in tmp_sku:
                        if (sku_1.color) != (result_sku_list[count-1]).color:
                            result_sku_list.append(sku_1)
                            count = count+1
                            break
        # if an motorbike just have 1 option, ket take all of it's color version
        else:
            result_sku_list.extend(tmp_skus)
            result_default_option.append(tmp_skus[0])

    result_brand_list       = list(set(result_brand_list))
    result_sku_list         = list(set(result_sku_list))
    result_default_option    = list(set(result_default_option))

    print(result_motor_list, "\n")
    print(result_brand_list, "\n")
    print(result_sku_list, "\n")
    print(result_default_option, "\n")

    # print(key_list)
    # print(input_str)

    return render(request, "search-text.html", {
        'brands': result_brand_list,
        'motorbikes': result_motor_list,
        'skus': result_sku_list,
        'default_option': result_default_option,
        'user': user,
    })

def search_brand(request, brand_id):
    user_id = request.session.get("user_id")
    user = None



    if (user_id):
        user = users.objects.get(user_id = user_id)

    target_brand_id = int(brand_id)
    target_brand = brands.objects.get(brand_id = target_brand_id)

    result_brand_list = []
    result_motor_list = []
    result_sku_list = []
    result_default_option = []


    result_brand_list.append(target_brand)
    result_motor_list.extend(list(motorbikes.objects.filter(brand = target_brand).order_by('motorbike_id')))


    #get unique color for unique option
    for motor in result_motor_list:
        tmp_skus = motorbike_skus.objects.filter(motorbike = motor).order_by('price')
        options = []

        for sku in tmp_skus:
            options.append(sku.option)

        options = list(set((options)))

        if len(options) > 1:
            tmp_options = [tmp_skus[0].option]
            result_sku_list.append(tmp_skus[0])
            result_default_option.append(tmp_skus[0])
            count = 1

            for sku in tmp_skus:
                tmp_option = sku.option
                if tmp_option not in tmp_options:
                    tmp_options.append(sku.option)
                    tmp_sku = tmp_skus.filter(option = tmp_option)
                    for sku_1 in tmp_sku:
                        if (sku_1.color) != (result_sku_list[count-1]).color:
                            result_sku_list.append(sku_1)
                            count = count+1
                            break
        # if an motorbike just have 1 option, ket take all of it's color version
        else:
            result_sku_list.extend(tmp_skus)
            result_default_option.append(tmp_skus[0])


    # motor_brands = get_brands()
    # motorbike_types = get_motor_types()

    return render(request, "search-text.html", {
        'brands': result_brand_list,
        'motorbikes': result_motor_list,
        'skus': result_sku_list,
        'default_option': result_default_option,
        'user': user,
        'brands_cat': get_brands(),
        'motorbike_types_cat': get_motor_types(),
    })


def search_type(request, type_id):
    user_id = request.session.get("user_id")
    user = None



    if (user_id):
        user = users.objects.get(user_id = user_id)

    target_type_id = int(type_id)
    target_type = motor_types.objects.get(type_id = target_type_id)

    result_brand_list = []
    result_motor_list = []
    result_sku_list = []
    result_default_option = []


    # result_brand_list.append(target_brand)
    result_motor_list.extend(list(motorbikes.objects.filter(type = target_type).order_by('motorbike_id')))
    result_brand_list.append((result_motor_list[0]).brand)


    #get unique color for unique option
    for motor in result_motor_list:

        # get brand
        if motor.brand not in result_brand_list:
            result_brand_list.append(motor.brand)

        tmp_skus = motorbike_skus.objects.filter(motorbike = motor).order_by('price')

        tmp_options = [tmp_skus[0].option]
        result_sku_list.append(tmp_skus[0])
        result_default_option.append(tmp_skus[0])
        count = 1

        for sku in tmp_skus:
            tmp_option = sku.option
            if tmp_option not in tmp_options:
                tmp_options.append(sku.option)
                tmp_sku = tmp_skus.filter(option = tmp_option)
                for sku_1 in tmp_sku:
                    if (sku_1.color) != (result_sku_list[count-1]).color:
                        result_sku_list.append(sku_1)
                        count = count+1
                        break

    # motor_brands = get_brands()
    # motorbike_types = get_motor_types()

    # sort result_brand_list by brand_order
    result_brand_list = sorted(result_brand_list, key=lambda brand: brand.brand_id)

    return render(request, "search-text.html", {
        'brands': result_brand_list,
        'motorbikes': result_motor_list,
        'skus': result_sku_list,
        'default_option': result_default_option,
        'user': user,
        'brands_cat': get_brands(),
        'motorbike_types_cat': get_motor_types(),
    })

def update_user_info(request):
    current_user = get_current_user(request)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        current_user.full_name = full_name
        current_user.address = address
        current_user.email = email


        changePassword = request.POST.get('changePassword')

        if changePassword == 'on':
            password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            if password == current_user.password:
                if new_password == confirm_new_password:
                    current_user.password = new_password
                    current_user.save()
                    return redirect("login")
                else:
                    return render(request, "update-user-info.html",{
                        'user': current_user,
                        'error': "Mật khẩu xác nhận không đúng"
                    })
            else:
                return render(request, "update-user-info.html",{
                    'user': current_user,
                    'error': "Mật khẩu cũ không đúng"
                })
        else:
            current_user.save()
            return redirect("home")

    else:
        return render(request, "update-user-info.html",{
            'user': current_user,
            'error': ""
        })