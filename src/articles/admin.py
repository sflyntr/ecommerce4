from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', )
    # prepopulated_fields = {'slug': ('title',)}
    # instead of this, use signal or model save override


admin.site.register(Article, ArticleAdmin)