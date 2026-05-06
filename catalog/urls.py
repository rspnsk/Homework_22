from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, contacts_us

app_name = CatalogConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('send-message/', contacts_us, name='contacts-us'),
]
