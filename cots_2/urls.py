from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orchestration/', views.orchestration),
    path('blue/', views.blue),
    path('red/', views.red),
    path('purple/', views.purple),
]
