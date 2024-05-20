from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import UserForm
from .models import users, brands, motorbikes, motorbike_skus
from django.http import HttpResponse


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
            result = users.objects.get(phone = user_phone)
            print("Result: ", result)
        except:
            print("No user match")
        return render(request, "login.html")
    else:
        # form = UserForm()
        # return render(request, "login.html", {"form" : form})
        return render(request, "login.html")


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
    })

def motor_detail(request, slug):
    motor = motorbikes.objects.get(model_slug = slug)
    motor_skus = motorbike_skus.objects.filter(motorbike = motor).order_by('price')

    option = []

    for sku in motor_skus:
        option.append(sku.option)
        if sku.color.color_3:
            pass
        else:
            print("-",sku.color.color_3,"-")

    option = list(set(option))

    print(option)

    # return HttpResponse("<h1>{model}</h1>".format(model = motorbike.model))
    return render(request, "product.html", {
        'motorbike': motor,
        'options': option,
        'skus': motor_skus,
    })

