import os
import random

from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q
from django.shortcuts import reverse

from ecommerce.utils import unique_slug_generator


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    filename, ext = os.path.splitext(basename)
    return filename, ext


def upload_image_path(instance, filepath):
    new_filename = random.randint(1, 324412123)
    name, ext = get_filename_ext(filepath)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return f"products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(active=True, featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query)|
                   Q(description__icontains=query)|
                   Q(price__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, in_id):
        qs = self.get_queryset().active().filter(id=in_id)
        if qs.exists() and qs.count() == 1:
            return qs.first()
        else:
            return None

    def search(self, query):
        return self.get_queryset().active().search(query)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=39.99)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    featured = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    @property
    def name(self):
        return self.title


def pre_save_product_sender(sender, instance, *args, **kwargs):
    print("in pre save")
    print(instance.slug)
    if instance.slug is None or instance.slug == '':
        print("slug is None")
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_product_sender, sender=Product)



