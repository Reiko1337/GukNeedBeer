from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, CharField, ValidationError, EmailField, EmailInput, ImageField, \
    FileInput
from django.contrib.auth import authenticate
from .ConfirmEmail import confirm
from django.contrib.auth import password_validation
from django import forms
from PIL import Image


class RegistrationForm(UserCreationForm):
    password1 = CharField(label='Пароль',
                          widget=PasswordInput(attrs={
                              'placeholder': 'Пароль',
                              'autocomplete': 'current-password',
                          })
                          )

    password2 = CharField(label='Подтверждение пароля',
                          widget=PasswordInput(attrs={
                              'placeholder': 'Подтверждение пароля',
                              'autocomplete': 'current-password',
                          })
                          )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                'placeholder': 'Имя пользователя',
                'autocomplete': 'off',
            }),
            'email': EmailInput(attrs={
                'placeholder': 'Почта',
                'autocomplete': 'off',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).all():
            raise ValidationError('Такой Email уже зарегистрирован')
        return self.cleaned_data['email']


class LoginForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={
        'placeholder': 'Имя пользователя',
        'autocomplete': 'off',
    }))

    password = CharField(widget=PasswordInput(attrs={
        'placeholder': 'Пароль',
        'autocomplete': 'current-password',
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                except:
                    user_temp = None

                if user_temp is not None and user_temp.check_password(password):
                    self.confirm_login_allowed(user_temp)
                else:
                    raise ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            confirm(self.request, user)
            raise ValidationError("Необходимо активировать аккаунт. "
                                  "Мы отправили вам сообщения на вашу почту {0}".format(user.email))


class PasswordReset(PasswordResetForm):
    email = EmailField(
        max_length=254,
        widget=EmailInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Почта'
        })
    )


class SetPassword(SetPasswordForm):
    new_password1 = CharField(
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Новый пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = CharField(
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Подтверждение нового пароля'}),
    )


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Имя',
                'autocomplete': 'off',
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Фамилия',
                'autocomplete': 'off',
            }),
        }


class PasswordChange(PasswordChangeForm):
    old_password = CharField(
        strip=False,
        widget=PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'placeholder': 'Старый пароль'
        }),
    )
    new_password1 = CharField(
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Новый пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = CharField(
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Подтверждение нового пароля'}),
    )


class ImageForm(forms.Form):
    MIN_RESOLUTION = (184, 184)
    MAX_RESOLUTION = (1000, 1000)
    MAX_SIZE = 3145728
    image = ImageField(label='Аватарка', required=False, widget=FileInput({
        'accept': '.png, .jpg',
        'class': 'input-file',
        'name': 'file',
        'id': 'file'
    }))

    def clean_image(self):
        if self.cleaned_data['image'] is None:
            raise ValidationError('')
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
