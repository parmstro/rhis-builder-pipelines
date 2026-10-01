from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.HealthView.as_view()),
    path('categories/', views.CategoryListView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('suppliers/', views.SupplierListView.as_view()),
    path('customers/', views.CustomerListView.as_view()),
    path('customers/<int:customer_id>/', views.CustomerDetailView.as_view()),
    path('customers/<int:customer_id>/orders/', views.CustomerOrdersView.as_view()),
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view()),
]
