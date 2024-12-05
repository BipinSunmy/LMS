from django.urls import path
from .views import Display,user_login,admin_dashboard
urlpatterns = [
    path("",Display,name="home"),
    path("login/",user_login,name="login"),
    path("admins/dashboard",admin_dashboard,name="admin_dashboard")
]