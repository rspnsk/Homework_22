from django import forms
from .models import Product, Category
from django.core.exceptions import ValidationError

forbid_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class ProductForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #     self.fields['image'].widget.attrs.update({'class': 'your-css-class'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Приводим имя к нижнему регистру
        name_lower = name.lower()
        for word in forbid_words:
            if word.lower() in name_lower:
                raise ValidationError('Запрещённое слово в имени продукта')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        description_lower = description.lower()
        for word in forbid_words:
            if word.lower() in description_lower:
                raise ValidationError('Запрещённое слово в описании продукта')
        return description

    def clean_price(self):
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
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите наименование продукта'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание продукта'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену продукта'})

class CategoryForm(forms.ModelForm):
    
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
