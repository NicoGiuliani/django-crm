from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("customer/<int:pk>", views.customer_record, name="customer"),
    path("delete/<int:pk>", views.delete_record, name="delete"),
    path("add/", views.add_record, name="add"),
]
