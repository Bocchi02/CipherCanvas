from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('encode/', views.encode, name='encode'),
    path('decode/', views.decode, name='decode'),
    path('verify/', views.verify, name='verify'),
    path('about/', views.about, name='about'),
]