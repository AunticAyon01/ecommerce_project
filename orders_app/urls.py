from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_history, name='order_history'),
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    path('all/', views.all_orders, name='all_orders'),
]
