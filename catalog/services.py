from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class ProductService:

    @staticmethod
    def get_products_by_category(category_id):
        """
        Возвращает список всех продуктов в указанной категории.
        Данные кешируются на 15 минут.
        """
        # 1. Формируем уникальный ключ для кеша
        cache_key = f'products_cat_{category_id}'

        # 2. Пытаемся получить данные из кеша
        products = cache.get(cache_key)

        # 3. Если в кеше ничего нет, идем в базу данных
        if products is None:
            # Находим категорию или отдаем 404
            category = get_object_or_404(Category, id=category_id)

            # Делаем запрос к БД и превращаем QuerySet в список (list).
            # Это необходимо, так как ленивый QuerySet целиком в кеш не запишется.
            products = list(
                Product.objects.filter(category=category).select_related('category')
            )

            # 4. Записываем результат в кеш на 900 секунд (15 минут)
            cache.set(cache_key, products, timeout=900)

        return products
