from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]
