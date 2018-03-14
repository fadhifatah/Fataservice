from django.urls import path
from . import views

urlpatterns = [
    path('ori/', views.image),
    path('thumb/', views.thumbnail),
]
