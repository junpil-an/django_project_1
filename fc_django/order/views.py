from django.shortcuts import render , redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from fcuser.decorators import login_required
from django.db import transaction
from .forms import RegisterForm
from .models import Order
from product.models import Product
from fcuser.models import Fcuser
# Create your views here.


@method_decorator(login_required, name ='dispatch')
class OrderCreate(FormView):
    
    form_class = RegisterForm
    success_url = '/product/'
    
    def form_valid(self, form):
    # 이안에서 db관련된 동작들은 transation으로 처리됨
        with transaction.atomic():
            prod = Product.objects.get(pk=form.data.get('product'))
            order = Order(
                quantity = form.data.get('quantity'),
                product = prod,
                #session 에 있는 이메일을 가지고 옴
                fcuser = Fcuser.objects.get(email =self.request.session.get('user')) 
            )

            order.save()
            #주문할 때 사용한 수량만큼 재고에섯 차감됨
            prod.stock -= int(form.data.get('quantity'))
            prod.save()
        
        return super().form_valid(form)


    #유효한 값이 아닐때 되돌아감
    def form_invalid(self, form):
        return redirect('/product/'+str(form.data.get('product')))

    #폼을 생성할 때 어떤인자값을 받아전달할지
    def get_form_kwargs(self,**kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request':self.request
        })
        return kw 

@method_decorator(login_required, name ='dispatch')
class OrderList(ListView):
    
    #사용자 전부 주문이 나옴
    #model = Order
    
    template_name = 'order.html'
    context_object_name = 'order_list'

    #사용자 쿼리셋을 오버라이딩해서 가져옴
    def get_queryset(self,**kwargs):
        # _ 를 2개 해줘야 함 fcuser 안에 __ email
        queryset = Order.objects.filter(fcuser__email = self.request.session.get('user'))
        return queryset

    