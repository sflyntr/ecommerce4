from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse

from ecommerce.utils import unique_slug_generator


class Article(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    # method 1. save() method override
    # def save() 로 하는 것인데 일단 주석처리 대신 이렇게 처리함.
    # 이 방식 이외에 signal 처리도 있고 form처리도 있다.
    def save_with_slug(self, *args, **kwargs):
        if not self.slug:
            # slug 는 unique check를 하지 않는다.
            # 단지 스페이스를 - 로 변경하는등 url로 사용가능한 문자로 바꾼다.
            # self.slug = slugify(self.title)
            self.slug = unique_slug_generator(self)
        return super().save(*args, **kwargs)


# mdthod 2. signal
def pre_save_article_sender(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_article_sender, sender=Article)
