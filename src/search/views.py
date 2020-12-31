from django.db.models import Q
from django.views.generic import ListView

from products.models import Product


class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = self.request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()

    def get_queryset_old(self, *args, **kwargs):
        request = self.request
        query = self.request.GET.get('q', None)
        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.filter(lookups).distinct()
        return Product.objects.featured()