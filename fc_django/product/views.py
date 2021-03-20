from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from django.views.generic.edit import FormView
from .models import Product
from .forms import ResisterProductForm
from order.forms import RegisterForm as OrderForm
from django.utils.decorators import method_decorator
from fcuser.decorators import admin_required

class ProductList(ListView):
    model = Product
    template_name = "product.html"

    #객체 이름 변경 기본은 objcet_list임
    context_object_name = 'Product'


@method_decorator(admin_required, name ='dispatch')
class ProductCreate(FormView):

    template_name = 'register_product.html'
    form_class = ResisterProductForm
    success_url = '/product/'

    def form_valid(self,form):
        product = Product(
        name = form.data.get('name'),
        price= form.data.get('price'),
        description = form.data.get('description'),
        stock = form.data.get('stock')
        )

        product.save()
        return super().form_valid(form)

class ProductDetail(DetailView):

    template_name = 'product_detail.html'
    #필요한 쿼리를 가져온다
    queryset = Product.objects.all()

    context_object_name = 'product'

    # 원하는 데이터를 넣을 수 있도록 함수 제공
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = OrderForm(self.request)
        return context
    