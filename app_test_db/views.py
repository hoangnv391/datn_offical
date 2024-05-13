from django.shortcuts import render
from .forms import UserForm

# Create your views here.
def login(request):
    if request.method == "POST":
        # form = UserForm(request.POST)
        # print(form['phone'].value())
        # return render(request, "login.html", {"form" : form})
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(phone)
        print(password)
        return render(request, "loginAndSignup.html", {
            "form_type": "login",
        })
    else:
        # form = UserForm()
        # return render(request, "login.html", {"form" : form})
        return render(request, "test.html", {
            "form_type": "login"
        })


def signup(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')

        print(phone)
        print(password)
        print(confirm_password)
        print(full_name)
        print(address)
        print(email)

        return render(request, "loginAndSignup.html", {
            "form_type": "signup",
        })

    else:
        return render(request, "loginAndSignup.html", {
            "form_type": "signup",
        })
