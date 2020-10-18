from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView)

from .serializers import (UserCreateSerializer, GYMCreateSerializer, ClassCreateSerializer,
                          UserLoginSerializer, GYMListSerializer, ClassesListSerializer, ClassesDetailSerializer)
from .models import GYM, Type, Classes, Booking


# Register


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

# Signin


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

# List of GYMs


class GYMListView(ListAPIView):
    queryset = GYM.objects.all()
    serializer_class = GYMListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]


# List of * all * classes


class AllClassesListView(ListAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]


# List of * new * classes


class NewClassesListView(ListAPIView):
    queryset = Classes.objects.filter(start__gt=now())
    serializer_class = ClassesListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]

# Detail of classes


class ClassDetails(RetrieveAPIView):
    queryset = Classes.objects.all()
    serializer_class = ClassesDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'class_id'
    permission_classes = [AllowAny]

# Create GYM


class CreateGYM(CreateAPIView):
    serializer_class = GYMCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# Create Class


class CreateClass(CreateAPIView):
    serializer_class = ClassCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        new_gym = GYM.objects.get(id=self.kwargs['gym_id'])
        new_gym.number_of_classes += 1
        new_gym.save()
        serializer.save(
            gym_id=self.kwargs['gym_id'], type_of_id=self.kwargs['type_id'])
