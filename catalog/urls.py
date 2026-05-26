from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import base
from .views import ProductsListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ContactsUsView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('send-message/', ContactsUsView.as_view(), name='contacts-us'),
    path('contact-us/', ContactsUsView.as_view(), name='contact_us'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
