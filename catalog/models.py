from django.db import models
from django.contrib.auth import get_user_model
from django.core.cache import cache


# используем get_user_model(), чтобы код работал и с кастомной моделью пользователя
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    owner = models.ForeignKey(
        User,  # Связываем с моделью пользователя
        on_delete=models.CASCADE,  # Если пользователь удален, его продукты тоже удаляются
        verbose_name='Владелец продукта',
        related_name='products',  # Позволит получить все продукты пользователя через user.products.all()
        blank = True,
        null = True  # null=True нужно, если в базе уже есть продукты без владельца
    )

    # Определяем константы для статусов
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED= 'published'
    STATUS_UNPUBLISHED = 'unpublished'

    # 2. Создаем список выбора
    PRODUCT_STATUSES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PUBLISHED, 'Опубликован'),
        (STATUS_UNPUBLISHED, 'Снят с публикации'),
    ]

    # 3. Добавляем новое поле со списком выбора
    published_status = models.CharField(
        verbose_name='Статус публикации',
        max_length=20,
        choices=PRODUCT_STATUSES,
        default=STATUS_DRAFT, # По умолчанию товар будет черновиком
    )

    # переопределяем метод save, чтобы сайт обновлялся мгновенно,
    # кеш нужно сбрасывать в момент сохранения или удаления продукта.
    def save(self, *args, **kwargs):
        # Перед сохранением формируем ключ кеша для категории этого продукта
        if self.category_id:
            cache_key = f'products_cat_{self.category_id}'
            cache.delete(cache_key)  # Удаляем старый кеш

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # При удалении продукта также очищаем кеш категории
        if self.category_id:
            cache_key = f'products_cat_{self.category_id}'
            cache.delete(cache_key)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['published_status']
        # Добавляем кастомные разрешения
        permissions = [
            ("can_unpublish_product", "может отменять публикацию продукта"),
            ("can_delete_product", "может удалять продукт"),
        ]

class ContactInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    country = models.CharField(max_length=100, verbose_name="Страна")
    inn = models.CharField(max_length=20, verbose_name="ИНН")
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
