from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('encode/', views.encode),
    path('decode/', views.decode),
    path('verify/', views.verify),
    path('about/', views.about),
]