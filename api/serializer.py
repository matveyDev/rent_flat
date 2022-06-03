from rest_framework import serializers
from arenda.models import Reservation
from flat.models import Flat, Image, Review
from arenda.models import Reservation
from rest_framework.reverse import reverse
from rest_auth.registration.serializers import RegisterSerializer
from django.core.validators import RegexValidator


class RegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(validators=[RegexValidator(regex='^\1?\d{9,11}$')], max_length=11, required=False)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
        }


class ReservationSerializer(serializers.ModelSerializer):
    update = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault()) #Авторизованный юзер

    class Meta:
        model = Reservation
        fields = [
            'id',
            'flat',
            'arenda_date',
            'update',
            'delete',
            'user',
        ]

    def get_update(self, obj):
        return reverse('api_reservation_update', args=(obj.pk,))

    def get_delete(self, obj):
        return reverse('api_reservation_delete', args=(obj.pk,))


class ReviewListSerializer(serializers.ModelSerializer):
    update = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'rating',
            'text',
            'created',
            'flat_review',
            'update',
            'delete',
        ]
    
    def get_update(self, obj):
        return reverse('api_review_update', args=(obj.pk,))

    def get_delete(self, obj):
        return reverse('api_review_delete', args=(obj.pk,))



class ReviewSerializer(serializers.ModelSerializer):
    update = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'rating',
            'text',
            'created',
            'update',
            'delete',
        ]
        
    def get_update(self, obj):
        return reverse('api_review_update', args=(obj.pk,))

    def get_delete(self, obj):
        return reverse('api_review_delete', args=(obj.pk,))


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ['image',]


class FlatListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Flat
        fields = [
            'id',
            'address',
            'empty',
            'photo',
            'absolute_url',
        ]
    
    def get_absolute_url(self, obj):
        return reverse('api_flat_detail', args=(obj.pk,))


class FlatDetailSerializer(serializers.ModelSerializer):
    photos = ImageSerializer(many=True, required=False)
    reviews = ReviewSerializer(many=True, required=False)
    reservations = ReservationSerializer(many=True, required=False)

    class Meta:
        model = Flat
        fields = [
            'id',
            'address',
            'empty',
            'photo',
            'photos',
            'reviews',
            'reservations',
        ]
