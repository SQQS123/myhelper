from django.urls import path
from . import views

urlpatterns = [
    path('', views.koutu, name='koutu'),
    path('upload/', views.upload_and_remove_bg, name='upload_and_remove_bg'),
]
