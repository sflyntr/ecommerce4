from django.conf.urls import url, include


from .views import ArticleDetailView, ArticleListView

urlpatterns = [
    url(r'^$', ArticleListView.as_view, name='article_list'),
    url(r'^(?P<slug>[\w-]+)/$', ArticleDetailView.as_view(), name='article_detail'),
]
