from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import UserForm
from .models import users, brands, motorbikes, motorbike_skus, motorbike_feature_images, motorbike_specs, cart_items
from django.http import HttpResponse, JsonResponse
import json

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