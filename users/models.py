from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):
    """ Кастомный менеджер для модели пользователя. Требуется, так как мы используем email вместо username. """

    def create_user(self, email, password=None, **extra_fields):
        """ Создает и сохраняет обычного пользователя с заданным email и паролем. """
        #             email (str): Адрес электронной почты пользователя.
        #             password (str, optional): Пароль пользователя. По умолчанию None.
        #             **extra_fields: Дополнительные поля для модели пользователя.
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты.')

        email = self.normalize_email(email)  # Приводит email к единому формату
        user = self.model(email=email, **extra_fields)  # Создаем экземпляр модели, но не сохраняем его в БД (commit=False)
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)  # Сохраняем пользователя в базу данных
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Создает и сохраняет суперпользователя с указанными email и паролем.
                Args:
                    email (str): Адрес электронной почты суперпользователя.
                    password (str): Пароль суперпользователя.
                    **extra_fields: Дополнительные поля для модели пользователя.
                Raises:
                    ValueError: Если флаги is_staff или is_superuser не True.
                Returns:
                    CustomUser: Созданный суперпользователь. """
        extra_fields.setdefault('is_staff', True) # is_staff отвечает за доступ в административную панель (/admin). True разрешает пользователю туда войти.
        extra_fields.setdefault('is_superuser', True) # is_superuser дает пользователю абсолютные права.
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'Admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields) # Вызываем наш новый метод create_user


class CustomUser(AbstractUser):
    """ Кастомная модель пользователя, использующая email в качестве логина.
    Убрано поле username, добавлены дополнительные поля. """
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    phone_number = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар',blank=True, null=True)
    country = CountryField(blank_label="Выберите страну", blank=True)

    USERNAME_FIELD = 'email' # Указываем, что поле email является логином (USERNAME_FIELD)
    REQUIRED_FIELDS = []     # REQUIRED_FIELDS определяет, какие поля будут запрошены при создании
                             # суперпользователя через команду createsuperuser. У нас их нет.

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = CustomUserManager() # Подключаем наш кастомный менеджер для работы с этой моделью

    def __str__(self):
        return self.email
