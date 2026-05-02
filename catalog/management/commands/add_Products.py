from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Add product to the database'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name='Электроника', description='техника и гаджеты')

        products = [
            {'name': 'Samsung', 'description': 'телефон', 'image': '', 'price': 600, 'created_at': '2026-04-30',
             'updated_at': '2026-04-30', 'category': category},
            {'name': 'Asus', 'description': 'ноутбук', 'image': '', 'price': 800, 'created_at': '2026-04-30',
             'updated_at': '2026-04-30', 'category': category},
            {'name': 'Рубин', 'description': 'телевизор', 'image': '', 'price': 200, 'created_at': '2026-04-30',
             'updated_at': '2026-04-30', 'category': category},
        ]

        for pro in products:
            product, created = Product.objects.get_or_create(**pro)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Успешно добавлен продукт {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт {product.name} уже существует'))