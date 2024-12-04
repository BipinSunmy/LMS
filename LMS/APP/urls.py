from django.urls import path
from .views import Display,user_login
urlpatterns = [
    path("",Display,name="home"),
    path("login/",user_login,name="login")
]