from django.contrib import admin
from .models import Fcuser

class FcuserAdmin(admin.ModelAdmin):

    # ',' 를 꼭 써야한다 문자로 인식함 , 튜플로 인식못함
    list_display= ('email',)

    # overiding 함수를 덮어 씌워 새로 정의를 내림
    def changelist_view(self,request,extra_context = None):

        extra_context = {"title":"사용자 목록"}    
        #원래 가지고있던 chagelist_view 함수를 호출 
        #self 넣어주면 에러
        return super().changelist_view(request,extra_context)

    def changeform_view(self, request, object_id = None, form_url = '', extra_context= None):
        product = Fcuser.objects.get(pk=object_id)
        extra_context = {'title' : f'{product.email} 수정'}
        return super().changeform_view(request, object_id , form_url , extra_context)



admin.site.register(Fcuser,FcuserAdmin)
admin.site.site_header = "'pill's code"
admin.site.index_title = "pill's code_index" 
admin.site.site_title="pill's code_title"