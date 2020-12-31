import os
import string
import random

from django.utils.text import slugify


def get_filename(path):
    return os.path.basename(path)


def random_string_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    size = random.size(30, 45)
    key = random_string_generator(size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_key_generator(instance)
    return key


def unique_order_id_generator(instance):
    new_order_id = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id)
    if qs_exists:
        return unique_order_id_generator(instance)
    return new_order_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(str(instance))

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug_str = "{slug}-{randstr}".format(slug=slug,
                                                 randstr=random_string_generator(4))
        return unique_slug_generator(instance, new_slug=new_slug_str)
    return slug
