from django.urls import path
from . import views

urlpatterns = [
    path('ori/', views.image),
    path('thumbnail/', views.thumb),
]
