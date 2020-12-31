from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"
