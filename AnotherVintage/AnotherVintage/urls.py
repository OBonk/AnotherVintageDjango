"""AnotherVintage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from . import views
from . import login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',views.about,name="about"),
    path('',views.index,name="index"),
    path('shop/',views.shop,name="shop"),
    path('stock/<int:pid>',views.individual_stock),
    path('stock/delete/<int:pid>',views.delete),
    path('stock/',views.stock_control,name="stock"),
    path('login/',login.loginRQ,name="login"),
    path('logout/',login.logoutRQ,name="logout"),
    path('account/',views.account,name="account"),
    path('register/',login.registerRQ,name="register"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('item/<int:itemno>',views.prodpage)
]
