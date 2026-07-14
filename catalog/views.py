from django.http import HttpResponse
from .models import Category, Product, ContactInfo
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, CategoryForm
from .services import ProductService
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden("У вас нет прав для снятие с публикации продукта.")

        # Логика рецензирования продукта
        product.published_status = 'unpublished'
        product.save()

        return redirect('catalog:product_detail', pk=product.pk)

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Фильтруем только опубликованные товары
        return Product.objects.filter(published_status=Product.STATUS_PUBLISHED)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        # метод автоматически назначает текущего авторизованного пользователя владельцем
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products_list')

    # Условие проверки: авторизованный юзер должен быть владельцем этого продукта или админом
    def test_func(self):
        product = self.get_object() # Получаем объект, который собираемся редактировать
        # Разрешаем доступ, если юзер — владелец ИЛИ суперпользователь
        return self.request.user == product.owner or self.request.user.is_superuser


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.can_delete_product'
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для удаления продукта.")

    # такая же проверка на владельца или админа, как и в Update
    def test_func(self):
        product = self.get_object() # Получаем объект, который собираемся редактировать
        # Доступ открыт, если:
        # 1. Пользователь — владелец
        # 2. Пользователь — суперпользователь
        # 3. У пользователя есть глобальное разрешение на удаление продуктов
        return (
                self.request.user == product.owner or
                self.request.user.is_superuser or
                self.request.user.has_perm('catalog.delete_product')
        )


class CategoryProductsView(ListView):
    """ Сервисная функция для работы с продуктами, которая возвращает список всех продуктов в указанной категории"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return ProductService.get_products_by_category(category_id)



class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = ContactInfo.objects.all()
        return context


class ContactsUsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/categories_list.html'
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:categories_list')

    def get_queryset(self):
        queryset = cache.get('category_queryset') # Попытка получить данные из кэша: Сначала пытаемся извлечь queryset из кэша по ключу 'category_queryset'.
        if not queryset:                          # Проверка наличия в кэше: Если данные найдены в кэше (if not queryset), они сразу же возвращаются.
            queryset = super().get_queryset()     # Получение и кэширование данных: Если данных в кэше нет, выполняется обращение к родительскому методу super().get_queryset() для получения полного набора данных.
            cache.set('category_queryset', queryset, 60 * 15)  # Кешируем данные на 15 минут
        return queryset

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html'
    success_url = reverse_lazy('catalog:categories_list')


class BaseView(TemplateView):
    template_name = 'base.html'
