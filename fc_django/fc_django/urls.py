"""fc_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from fcuser.views import index , logout, RegisterView, LoginView
from product.views import ProductList , ProductCreate, ProductDetail, ProductListAPI, ProductDetailAPI
from order.views import OrderCreate , OrderList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    # class 같은 경우는 as_view 라는 함수를 사용해줘야함
    path('register/',RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',logout),
    path('product/',ProductList.as_view()),
    path('product/create/',ProductCreate.as_view()),
    #url 접근 상품이 나와야 함 , 숫자형이 pk 변수로 만들어져 전달이 됨
    path('product/<int:pk>/',ProductDetail.as_view()),
    path('order/create/',OrderCreate.as_view()),
    path('order/',OrderList.as_view()),

    path('api/product/',ProductListAPI.as_view()),
    path('api/product/<int:pk>', ProductDetailAPI.as_view()),
]
