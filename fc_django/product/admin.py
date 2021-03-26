from django.contrib import admin
from .models import Product
from django.utils.html import format_html
#숫자를 1000단위로 보기 편하게 변환시켜줌
from django.contrib.humanize.templatetags.humanize import intcomma

class ProductAdmin(admin.ModelAdmin):

    list_display= ('name','comma_price','styled_stock')

    # def comma_price(self,obj):

    #     return format(obj.price,',')

    def comma_price(self,obj):
        price = intcomma(obj.price)
        return f'{price} 원'

    def styled_stock(self,obj):

        if obj.stock <=20:

            return format_html(f'<b><span style  = "color:red">{intcomma(obj.stock)}</span></b> 개')

        return f'{intcomma(obj.stock)} 개'

    def changelist_view(self, request, extra_context = None):

        extra_context = {"title":"상품 목록"} 

        return super().changelist_view(request,extra_context)

    # 폼 수정하기 
    #어떤 objcet_id 가 필요
    def changeform_view(self, request, object_id = None, form_url = '', extra_context= None):
        product = Product.objects.get(pk=object_id)
        extra_context = {'title' : f'{product.name} 수정'}
        return super().changeform_view(request, object_id , form_url , extra_context)

    
    comma_price.short_description = '가격'
    styled_stock.short_description = '재고'

admin.site.register(Product,ProductAdmin)
