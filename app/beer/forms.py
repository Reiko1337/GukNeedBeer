from django import forms
from .models import Beer
from PIL import Image


class BeerForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ['name', 'price', 'rating', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название пиво',
                'autocomplete': 'off',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Цена',
                'autocomplete': 'off',
                'min': '0'
            }),
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Оценка',
                'autocomplete': 'off',
                'min': '0',
                'max': '10',
            }),
            'image': forms.FileInput(attrs={
                'id': 'uploadImage',
                'onchange': 'PreviewImage();'
            }),
        }

    MAX_SIZE = 3145728
    MIN_RESOLUTION = (184, 184)
    MAX_RESOLUTION = (2000, 2000)

    def clean_image(self):
        if self.cleaned_data['image'] is None:
            raise forms.ValidationError('')
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_h, min_w = self.MIN_RESOLUTION
        max_h, max_w = self.MAX_RESOLUTION
        max_size = self.MAX_SIZE
        if image.size > max_size:
            raise forms.ValidationError('Размер изображения не должен превышать 3MB')
        if img.height < min_h or img.width < min_w:
            raise forms.ValidationError('Разрешение изображени должно составлять 184 x 184 пикселя')
        if img.height > max_h or img.width > max_w:
            raise forms.ValidationError('Разрешение изображени не должно превышать 1000 x 1000 пикселей')
        return image


class SortBeerForm(forms.Form):
    ordering = forms.ChoiceField(label='Сортировка', required=False, choices=[
        ['name', 'От А-Я'],
        ['-name', 'От Я-А'],
        ['-price', 'Дорогие'],
        ['price', 'Дешевые'],
        ['-rating', 'Популярны'],
        ['rating', 'Не популярные'],
    ], widget=forms.Select(attrs={
        'class': 'select'
    }))
