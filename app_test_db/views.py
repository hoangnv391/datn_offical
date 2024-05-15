from django.shortcuts import render, redirect
from .forms import UserForm
from .models import users, brands, motorbikes, motorbike_skus

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
    motorbike_list = motorbikes.objects.all()

    print(motorbike_list)

    return render(request, "hometest.html", {
        'brands': motor_brands,
        'motorbikes': motorbike_list,

    })


