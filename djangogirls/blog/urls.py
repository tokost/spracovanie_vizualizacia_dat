from django.urls import path
from . import views


urlpatterns = [
    # pridanie URL pre post_list views
    path('', views.post_list, name='post_list'),
    # pridanie URL pre post_detail views
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # pridanie URL pre post_new views
    path('post/new/', views.post_new, name='post_new'),
]


