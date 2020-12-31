from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render

from .forms import ContactForm, LoginForm, RegisterForm
from products.models import Product


def home_page(request):
    object_list = Product.objects.featured()
    premium_contents = ",".join(obj.title for obj in object_list)
    context = {
        "title": "Home Page",
        "content": "Hello, World!!! It's working",
        "premium_contents": premium_contents
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content": "Welcome to Contact Page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, "contact/view.html", context)


def contact_page_with_pure_html(request):
    context = {
        "title": "Contact Page",
        "content": "Welcome to Contact Page!!!",
    }

    if request.method == "POST":
        print(request.POST)

    return render(request, "contact/view.html", context)


def about_page(request):
    context = {
        "title": "About page",
        "content": "Welcome to About Page!!!"
    }
    return render(request, "about.html", context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "title": "Register Page",
        "content": "Welcome to Register Page",
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = User.objects.create_user(username=username, email=email, password=password)
        if user is not None:
            print("Register Success")
            return redirect("/login")
        else:
            print("Register Error")

    return render(request, "auth/register.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "title": "Login Page",
        "content": "Welcome to Login Page",
        "form": form,
    }

    print("login_page")
    print(request.user.is_authenticated())

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        print(username+","+password)
        print("before auth")
        print(request.user.is_authenticated())
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("after auth")
            print(request.user.is_authenticated())
            login(request, user)
            return redirect("/")
        else:
            print("Login Error")

    return render(request, "auth/login.html", context)
