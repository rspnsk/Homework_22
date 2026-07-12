from django.urls import path, include
from catalog.apps import CatalogConfig
from .views import (ProductsListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
                    ContactsUsView, ContactsView, CategoryCreateView, CategoryUpdateView, CategoryListView,
                    UnpublishProductView,CategoryProductsView)

app_name = 'catalog'

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories_list'),
    path('category/new/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:category_id>/products/', CategoryProductsView.as_view(), name='category_products'),

    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('send-message/', ContactsUsView.as_view(), name='contacts-us'),
    path('contact-us/', ContactsUsView.as_view(), name='contact_us'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/unpublish/', UnpublishProductView.as_view(), name='product_unpublish'),
]
