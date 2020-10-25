from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import InfoUser
from PIL import Image


class EmailValidator(ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Такой Email уже зарегистрирован')
        return email


class ImageValidator(ModelForm):
    MIN_RESOLUTION = (184, 184)
    MAX_RESOLUTION = (1000, 1000)
    MAX_SIZE = 3145728

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_h, min_w = self.MIN_RESOLUTION
        max_h, max_w = self.MAX_RESOLUTION
        max_size = self.MAX_SIZE
        if image.size > max_size:
            raise ValidationError('Размер изображения не должен превышать 3MB')
        if img.height < min_h or img.width < min_w:
            raise ValidationError('Разрешение изображени должно составлять 184 x 184 пикселя')
        if img.height > max_h or img.width > max_w:
            raise ValidationError('Разрешение изображени не должно превышать 1000 x 1000 пикселей')
        return image


class ImageInline(admin.StackedInline):
    model = InfoUser
    can_delete = False
    verbose_name_plural = 'Аватарка'
    form = ImageValidator


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    inlines = (ImageInline,)
    form = EmailValidator


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(InfoUser)
