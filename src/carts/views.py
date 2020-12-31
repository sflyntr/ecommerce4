from django.shortcuts import render, redirect

from .models import Cart
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile, GuestEmail
from products.models import Product
from orders.models import Order

def cart_create(user=None):
    cart_obj = Cart.objects.create(user=user)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    print("cart_upate: {}".format(product_id))

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExists:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()

    return redirect("cart:home")


# 이 함수는 billing정보도 있어야 한다.

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None

    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    user = request.user
    billing_profile = None

    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')


    # Billing Profile을 만든다.
    # 항상 사용자 정보는 1순위가 request.user 가 인증되었다면 그게 우선이다.
    # 그 다음이 guest정보이다.
    if user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass

    # 이하는 사실 Order 모델을 만든뒤에 진행한다.
    # Checkout 시 context에 order, billing_profile, loginform, guestform 등을 넣기 위함이다.
    # 실제 Order안에는 billing_profile이 foreign key로 있는데 써야 하나?
    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form
    }

    return render(request, "carts/checkout.html", context)

