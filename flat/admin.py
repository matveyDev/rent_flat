from django.utils.safestring import mark_safe
from django.contrib import admin
from django import forms
from .models import Flat, Review, Image

class FlatAdminForm(forms.ModelForm):
  class Meta:
    model = Flat
    fields = '__all__'


class ReviewAdminForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = '__all__'


class ImageAdminForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = '__all__'


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    form = FlatAdminForm
    list_display = ('address', 'empty',)
    search_fields = ('address', 'pk', )
    fields = ('city', 'address', 'zip_code', 'empty', 'photo', 'get_photo',)
    readonly_fields = ('empty', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return "Нет фото"
    
    get_photo.short_description = "Фото"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ('flat', 'author', 'rating', 'created')
    search_fields = ('flat', 'author', 'rating', 'created')
    fields = ('flat', 'author', 'rating', 'text', 'created')
    readonly_fields = ('flat', 'author', 'created')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    list_display = ('flat', 'image',)
    fields = ('flat', 'image', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return "Нет фото"

    get_image.short_description = "Фото"