from django import forms
from .models import Product, Category
from django.core.exceptions import ValidationError


# Список запрещённых слов для проверки
forbid_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class ProductForm(forms.ModelForm):
    """ Форма для создания и редактирования продуктов.
        Включает валидацию полей: имени, описания и цены.
        Применяет проверку на запрещённые слова, а также проверяет,
        что цена является положительным числом.
        Полям назначаются CSS-классы и плейсхолдеры. """

    def clean_name(self):
        """ Валидация поля 'name'.
        Метод очистки поля "Имя" от возможного содержания запрещенных слов """

        name = self.cleaned_data.get('name')
        # Приводим имя к нижнему регистру
        name_lower = name.lower()
        for word in forbid_words:
            if word.lower() in name_lower:
                raise ValidationError('Запрещённое слово в имени продукта')
        return name

    def clean_description(self):
        """ Валидация поля 'description'.
        Метод очистки поля "Описание" от возможного содержания запрещенных слов """

        description = self.cleaned_data.get('description')
        description_lower = description.lower()
        for word in forbid_words:
            if word.lower() in description_lower:
                raise ValidationError('Запрещённое слово в описании продукта')
        return description

    def clean_price(self):
        """Валидатор цены товара (должна превышать ноль)"""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Цена должна быть положительной')
        return price

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена за покупку'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """ Инициализация формы.
            Добавляет CSS-класс 'form-control' и плейсхолдеры ко всем полям. Вызывает родительский конструктор. """
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите наименование продукта'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание продукта'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену продукта'})

class CategoryForm(forms.ModelForm):
    """ Форма для создания и редактирования категорий.
    Содержит поля 'name' и 'description'. Полям назначаются CSS-классы и плейсхолдеры.
    Описание отображается в многострочном текстовом поле (textarea)."""

    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите наименование категории'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание категории'})
