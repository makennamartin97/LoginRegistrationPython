from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('registerUser', views.register),
    path('loginUser', views.login),
    path('success', views.success),
    path('logout', views.logout),
]