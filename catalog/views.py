from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ContactInfo
from django.shortcuts import render, redirect
from .forms import ProductForm


def home(request):
    # Получаем последние 3 созданных продукта
    latest_products = Product.objects.order_by('-created_at')[:3]

    # Выводим их в консоль
    for product in latest_products:
        print(f"{product.name} - {product.price} руб.")  # или другой вывод, который нам нужен
    context = {'latest_products': latest_products}
    return render(request, 'catalog/home.html', context)

def contacts_us(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        message = request.POST.get('message')
        # Здесь мы просто возвращаем простой ответ
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')


def contacts(request):
    contacts = ContactInfo.objects.all()
    return render(request, 'catalog/contacts.html', {'contacts': contacts})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/product_list.html', context)

def base(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/base.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})