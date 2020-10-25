from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from pathlib import Path


def user_directory_path(instance, filename):
    return 'beer_image/{0}_{1}{2}'.format(instance.name, instance.user.id, Path(filename).suffix)


class Beer(models.Model):
    image = models.ImageField(verbose_name='Фото', blank=False, upload_to=user_directory_path)
    name = models.CharField(max_length=50, verbose_name='Название пиво')
    price = models.DecimalField(verbose_name='Цена', validators=[MinValueValidator(0)], max_digits=9, decimal_places=2)
    rating = models.PositiveIntegerField(verbose_name='Оценка',
                                         validators=[MinValueValidator(0), MaxValueValidator(10)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')

    class Meta:
        verbose_name = 'Пиво'
        verbose_name_plural = 'Пиво'
        ordering = ['-id']

    def __str__(self):
        return '{0}|{1}'.format(self.name, self.user.username)
