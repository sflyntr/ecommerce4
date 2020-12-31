from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# 이렇게 해도 된다. generic에 init.py에 shortcut이 있으므로,
# from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from carts.models import Cart

from .models import Product


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    # 아래와 같이 objects 하면 ModelManager가 나오고 all()을 하면 QuerySet이 나온다.
    # 그 QuerySet에는 featured 속성 없다고 나온다.
    # 즉, 우리는 ProductManager라는 Custome을 사용한 것 처럼
    # CustomerQuerySet을 만들어서 사용해야 한다.
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"


# Create your views here.
class ProductListView(ListView):
    # queryset = Product.objects.all()
    # 참고로 Class based view 에서 default view 이름은 product(모델명소문자)_list.html이다.
    # 따라서 template_name = "products/list.html" 로 하고 아무것도 안만들면,
    # product_list.html, list.html 2개의 template이 없다는 에러가 나온다. (Tip!!)
    # 실제 ListView 소스를 보면 template을 못찾는 경우, get_template_names 를 호출해서 default template을 찾는다.
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

class ProductListView_queryset_override(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk)


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

class ProductDetailView_queryset_override(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"
    hello_words = "Hello, World welcome to django world."

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("Product dosen't exist.....")
    #     return instance

    def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk)


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Hummmmm.")

        return instance


class ProductDetailView(DetailView):
    # get_object_or_404 안해도 DetailView나온다.즉, 어떤모델의 queryset을 사용하는지만 지정해도 된다.
    # 그리고 queryset 이름도 지정된거 써야한다. queryset = 말고 qs = 이런식으로 하면 안된다.
    # 즉, queryset이라는 변수에 반드시 model queryset을 지정해줘야 parent에서 그걸 참조한 함수들을 사용할 수 있다.
    queryset = Product.objects.all()
    # 참고로 Class based view 에서 default view 이름은 product(모델명소문자)_list.html이다.
    # 따라서 template_name = "products/list.html" 로 하고 아무것도 안만들면,
    # product_list.html, list.html 2개의 template이 없다는 에러가 나온다. (Tip!!)
    # 실제 ListView 소스를 보면 template을 못찾는 경우, get_template_names 를 호출해서 default template을 찾는다.
    template_name = "products/detail.html"
    hello_words = "Hello, World welcome to django world."

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


    # DetailView를 상속받음.
    # class DetailView(SingleObjectTemplateResponseMixin, BaseDetailView) <- BaseDetailView를 상속받음.
    # class BaseDetailView(SingleObjectMixin, View) <- SingleObjectMixin을 상속받음.
    # class SingleObjectMixin(ContextMixin) <- 여기에 get_object, get_context_data 등 정의되어 있음.
    # 이것을 재정의 하는 것임.

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product dosen't exist")
        return instance


def product_detail_view(request, pk=None, *args, **kwargs):
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exists")

def product_detail_view_old(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk, featured=True)

    # 아래도 동일한 기능을 수행한다.
    # instance = get_object_or_404(Product, pk=pk, featured=True)

    # 이것도 동일한 기능을 수행한다.
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExists:
    #     print('no product here')
    # except:
    #     print("huh?")

    qs = Product.objects.filter(id=pk)

    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist")


    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)

