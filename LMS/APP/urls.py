from django.urls import path
from .views import home,user_login,admin_dashboard,registration_view,user_logout,manageauthor_view,managebooks_view,manageuser,addbook,book_details
urlpatterns = [
    path("",home,name="home"),
    path("login/",user_login,name="login"),
    path("librarian/dashboard/",admin_dashboard,name="admin_dashboard"),
    path("register/",registration_view,name="registration"),
    path("logout/",user_logout,name = "logouts"),
    path("manage_user/",manageuser,name="mu"),
    path("manage_author/",manageauthor_view,name = "ma"),
    path("manage_books/",managebooks_view,name="mb"),
    path("addbooks/",addbook,name= "addbook"),
    path("book_details/<int:id>/",book_details,name="book_details")
]