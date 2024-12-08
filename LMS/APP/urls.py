from django.urls import path
from .views import home, user_login, admin_dashboard, registration_view, user_logout, manageauthor_view, managebooks_view, manageuser, addbook, book_details
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", user_login, name="login"),  # Main login path
    path("login/", user_login, name="login"),  # Redundant, can be kept or removed as needed
    path("home/", login_required(home), name="home"),  # Protected home page
    path("librarian/dashboard/", login_required(admin_dashboard), name="admin_dashboard"),
    path("register/", registration_view, name="registration"),
    path("logout/", user_logout, name="logout"),  # Logout path
    path("manage_user/", login_required(manageuser), name="mu"),  # Protecting the manage user view
    path("manage_author/", login_required(manageauthor_view), name="ma"),  # Protecting the manage author view
    path("manage_books/", login_required(managebooks_view), name="mb"),  # Protecting the manage books view
    path("addbooks/", login_required(addbook), name="addbook"),  # Protecting the add book view
    path('user_profile/', login_required(views.user_profile), name='user_profile'),
    path('edit_profile/', login_required(views.edit_profile), name='edit_profile'),
    path('change_password/', login_required(views.change_password), name='change_password'),
    path('wishlist/', login_required(views.wishlist), name='wishlist'),
    path('cart/', login_required(views.cart), name='cart'),
    path('add-to-cart/<int:book_id>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', login_required(views.remove_from_cart), name='remove_from_cart'),
    path('cart/update_quantity/<int:cart_item_id>/', login_required(views.update_quantity), name='update_quantity'),
    path('subscribe/', login_required(views.subscribe_view), name='subscribe'),
    path('make_payment/', login_required(views.make_payment), name='make_payment'),
    path("book_details/<int:id>/", book_details, name="book_details")  # No need for login protection here
]
