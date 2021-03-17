from django.contrib import admin
from .models import Fcuser

class FcuserAdmin(admin.ModelAdmin):

    # ',' 를 꼭 써야한다 문자로 인식함 , 튜플로 인식못함
    list_display= ('email',)

admin.site.register(Fcuser,FcuserAdmin)