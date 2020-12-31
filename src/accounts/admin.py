from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import GuestEmail


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email',]
    class Meta:
        model = User


admin.site.register(User)


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email', ]
    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)
