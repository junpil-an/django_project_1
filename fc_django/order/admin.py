from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from .models import Order
from django.template.response import TemplateResponse
from django.urls import path
# html escape -  tag 자체도 html에 보일 수 있게 만들어줌
# formats_html을 사용해 태그를 안에 넣어줄 수 있음
from django.utils.html import format_html
from django.db.models import F , Q
from django.db import transaction
import datetime

def refund(modeladmin,request , queryset):

    #한 트랜잭션 안에 넣어둠
    with transaction.atomic():
        # Q를 사용해 환불이 아닌것들을 필터로 가져올 수 있음
        qs = queryset.filter(~Q(status ='환불'))

        #무슨모델인지
        ct = ContentType.objects.get_for_model(qs.model)    

        for obj in qs:
            # if obj.status == '환불' :
            #     continue
            obj.product.stock += obj.quantity
            obj.product.save()

            #contenttype에 가지고있는 정보를 가져옴
            LogEntry.objects.log_action(
                user_id = request.user.id,
                content_type_id = ct.pk,
                object_id = obj.pk,
                object_repr = '주문 환불',
                action_flag = CHANGE,
                change_message= '주문 환불'
            )

        #쿼리셋을 환불로 변경해줌
        qs.update(status = '환불')

#상태 이름 변경
refund.short_description = '환불'

class OrderAdmin(admin.ModelAdmin):

    # ',' 를 꼭 써야한다 문자로 인식함 , 튜플로 인식못함
    list_display= ('fcuser','product','styled_status','action')
    #특정 필터값을 볼수 있다
    list_filter = ('status',)

    change_list_template = 'admin/order_chage_list.html'
    change_form_template = 'admin/order_chage_form.html'
    #액션값을 정의해줌
    actions = [
        refund
    ]

    def action(self, obj):
        if obj.status != '환불':
            return format_html(f"<input type='button' value = '환불' onclick='order_refund_submit({obj.id})' class ='btn btn-primary btn-sm'>")

    def styled_status(self,something):

        if something.status == 'hhjg627':
            
            #원하는 곳에 스타일링을 할 수 있음
            return format_html(f'<span style ="color:red">{something.status}</span>')
        
        return something.status

        # overiding 함수를 덮어 씌워 새로 정의를 내림
    def changelist_view(self,request, extra_context = None):
        
        extra_context = {"title":"주문 목록"}    
       
        if request.method == 'POST':
            print(request.POST)
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Order.objects.filter(pk=obj_id)

            ct = ContentType.objects.get_for_model(qs.model)    

            for obj in qs:
                obj.product.stock += obj.quantity
                obj.product.save()

                LogEntry.objects.log_action(
                    user_id = request.user.id,
                    content_type_id = ct.pk,
                    object_id = obj.pk,
                    object_repr = '주문 환불',
                    action_flag = CHANGE,
                    change_message= '주문 환불'
                )
            qs.update(status = '환불')

        #원래 가지고있던 chagelist_view 함수를 호출 
        return super().changelist_view(request,extra_context)

    def changeform_view(self, request, object_id = None, form_url = '', extra_context= None):
        order = Order.objects.get(pk=object_id)
        extra_context = {'title' : f'{order.fcuser.email} 의 {order.product.name} 수정'}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id , form_url , extra_context)

    def get_urls(self):
        urls= super().get_urls()
        date_urls = [
            path('date_view/', self.date_view),
        ]
        
        return date_urls + urls
    #새로 만들 템플릿
    def date_view(self, request):
        #현재 날짜에서 7일전 날짜를 뺌
        week_date = datetime.datetime.now() - datetime.timedelta(days=7)
        week_data = Order.objects.filter(register_date__gte = week_date)
        data = Order.objects.filter(register_date__lt=week_date)
        context = dict(
            #site에 정보값들을 요청받아 가져옴
            self.admin_site.each_context(request),
            week_data = week_data,
            data = data,
        )
        return TemplateResponse(request, 'admin/order_date_view.html', context)


    #함수 col 명 바꿔줄 수 있음x
    styled_status.short_description = '상태'

admin.site.register(Order,OrderAdmin)