from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Создает суперпользователя.'

    def handle(self, *args, **options):
        User = get_user_model()
        # Используем метод create_superuser из менеджера модели
        try:
            User.objects.create_superuser(
                email='admin@sky.pro',
                password='1234'
            )
            self.stdout.write(self.style.SUCCESS('Суперпользователь успешно создан.'))
        except Exception as e:
            # если пользователь с таким email уже существует
            self.stdout.write(self.style.ERROR(f'Ошибка при создании суперпользователя:{e}'))
