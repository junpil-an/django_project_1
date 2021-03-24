from django.contrib import admin
from .models import Order
# html escape -  tag 자체도 html에 보일 수 있게 만들어줌
# formats_html을 사용해 태그를 안에 넣어줄 수 있음
from django.utils.html import format_html

class OrderAdmin(admin.ModelAdmin):

    # ',' 를 꼭 써야한다 문자로 인식함 , 튜플로 인식못함
    list_display= ('fcuser','product','styled_status')
    #특정 필터값을 볼수 있다
    list_filter = ('status',)

    def styled_status(self,something):

        if something.status == 'hhjg627':
            
            #원하는 곳에 스타일링을 할 수 있음
            return format_html(f'<span style ="color:red">{something.status}</span>')

    #함수 col 명 바꿔줄 수 있음
    styled_status.short_description = '상태'
admin.site.register(Order,OrderAdmin)