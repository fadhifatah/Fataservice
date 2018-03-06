from django.urls import path
from . import views

urlpatterns = [
    path('users/login', views.login),
    path('users/register', views.register),
    path('users/', views.get_users),
    path('comments/create', views.create_comment),
    path('comments/<int:comment_id>/', views.get_comment_by_id),
    path('comments', views.get_comments),
    path('comments/delete', views.delete_comment),
    path('comments/update', views.update_comment),
]
