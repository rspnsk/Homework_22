from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу и назначает права.'

    def handle(self, *args, **kwargs):
        # 1. Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # 2. Получаем разрешения
        unpublish_permission = Permission.objects.get(codename='can_unpublish_product')
        delete_permission = Permission.objects.get(codename='delete_product')

        # 3. Привязываем права к группе
        group.permissions.add(unpublish_permission, delete_permission)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана, права назначены.'))
        else:
            self.stdout.write(self.style.SUCCESS('Права группы "Модератор продуктов" успешно обновлены.'))
