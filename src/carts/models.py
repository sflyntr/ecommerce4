from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.model.objects.filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.model.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None and user.is_authenticated():
            user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    # user, products(m2m), subtotal, total, updated, timestamp
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_save_cart_reciever(sender, instance, action, *args, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
        print("cart m2m received")
        products = instance.products.all()
        subtotal = 0.00
        for x in products:
            subtotal += float(x.price)
        if subtotal != instance.subtotal:
            instance.subtotal = subtotal
            instance.save()


m2m_changed.connect(m2m_save_cart_reciever, sender=Cart.products.through)


def pre_save_cart_reciever(sender, instance, *args, **kwargs):
    print("cart pre save 1")
    if instance.subtotal > 0:
        instance.total = float(instance.subtotal) * 1.1
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_reciever, sender=Cart)
