from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, contacts_us, product_detail, product_list, base, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('send-message/', contacts_us, name='contacts-us'),
    path('product_list/', product_list, name='product_list'),
    path('base/', base, name='base'),
    path('product_detail/<int:product_id>', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
]
