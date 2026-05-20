from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
]
