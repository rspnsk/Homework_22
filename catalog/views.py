from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, ContactInfo


def home(request):
    # Получаем последние 3 созданных продукта
    latest_products = Product.objects.order_by('-created_at')[:3]

    # Выводим их в консоль
    for product in latest_products:
        print(f"{product.name} - {product.price} руб.")  # или другой вывод, который вам нужен
    context = {'latest_products': latest_products}
    return render(request, 'home.html', context)

def contacts_us(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        message = request.POST.get('message')
        # Обработка данных (например, сохранение в БД, отправка email и т. д.)
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'contacts.html')


def contacts(request):
    contacts = ContactInfo.objects.all()
    return render(request, 'contacts.html', {'contacts': contacts})
