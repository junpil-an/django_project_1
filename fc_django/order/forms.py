from django import forms
from .models import Order
from product.models import Product
from fcuser.models import Fcuser
from django.db import transaction

class RegisterForm(forms.Form):

    #requset session을 전달 할 수 있게
    #생성자 함수
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


    quantity = forms.IntegerField(error_messages={'required':'수량을 입력하세요'},
    label = '수량')
    
    #실제로 사용자에게 보이지 않도록
    product = forms.IntegerField(error_messages={'required':'상품설명을 입력하세요'},
    label = '상품설명', widget = forms.HiddenInput)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        #session 안에 있는 user를 가져옴
        fcuser = self.request.session.get('user')


        if not(quantity and product ):
            
            self.add_error("product", "값이 없습니다")
            self.add_error("fcuser", "값이 없습니다")
            
