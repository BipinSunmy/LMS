from django.urls import path
from .views import Display

urlpatterns = [
    path("",Display)
]