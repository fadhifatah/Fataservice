from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_zip'),
    path('compression/', views.compression, name='compression')
]
