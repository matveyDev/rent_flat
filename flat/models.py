from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth import get_user_model

class Flat(models.Model):
    city = models.CharField(max_length=124, verbose_name='Гроод')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    zip_code = models.PositiveIntegerField(verbose_name='Почтовый индекс')
    empty = models.BooleanField(default=True, verbose_name='Свободна:')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Фото')

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('flat_detail', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        ordering = ['-id']


class Review(models.Model):
    flat = models.ForeignKey(Flat, verbose_name='Квартира', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), verbose_name='Автор', related_name='author', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг')
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)

    def get_absolute_url(self):
        return reverse('review', kwargs={"review_id": self.pk})

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']


class Image(models.Model):
    flat = models.ForeignKey(
        Flat, verbose_name='Квартира', related_name='photos',
        on_delete=models.CASCADE, blank=True, null=True,
    )
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return str(self.image)

    def get_absolute_url(self):
        return 'media/' + str(self.image)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'