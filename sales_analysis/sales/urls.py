from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-product', views.AddProductCreateView.as_view(), name='add_product'),
    path('add-customer', views.AddCustomerCreateView.as_view(), name='add_customer'),
    path('add-order', views.AddOrderCreateView.as_view(), name='add_order'),
    path('success', views.FormSuccessView.as_view(), name='form_success'),
]