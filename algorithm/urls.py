from django.urls import path
from . import views

urlpatterns = [
    path('plus/', views.plus),
    path('times/', views.times),
]
