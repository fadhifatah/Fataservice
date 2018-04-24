from django.urls import path
from . import views

urlpatterns = [
    path('plus/', views.plus),
    path('times/', views.times),
    path('mystery/', views.index, name='index'),
    path('green/', views.green),
    path('r1/', views.r1),
    path('r2/', views.r2),
    path('r3/', views.r3),
]
