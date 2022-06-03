from .serializer import ReviewListSerializer, ReviewSerializer,\
    FlatListSerializer, FlatDetailSerializer, ReservationSerializer
from rest_framework import generics
from flat.models import Flat, Review
from arenda.models import Reservation
from .permissions import IsAuthorOrReadOnly
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated


class ReservationCreateAPIView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated, )


class ReservationDestroyAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )


class ReservationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )
    serializer_class = ReservationSerializer


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class ReviewRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Review.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )
    serializer_class = ReviewSerializer


class ReviewDestroyAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = Review.objects.all()
    permission_classes = (IsAuthorOrReadOnly, )


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class FlatListAPIView(generics.ListAPIView):
    queryset = Flat.objects.all()
    serializer_class = FlatListSerializer


class FlatRetrieveAPIView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Flat.objects.all()
    serializer_class = FlatDetailSerializer
    parser_classes = (MultiPartParser, )