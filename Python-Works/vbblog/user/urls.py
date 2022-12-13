from django.contrib import admin
from django.urls import path
from . import views # bulunduğumuz klasörden al. 

app_name = "user" # uygulmaya isim verelim.
urlpatterns = [
    path('register/', views.register, name = "register"),
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
]
