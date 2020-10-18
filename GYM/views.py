from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView)

from .serializers import (UserCreateSerializer,
                          UserLoginSerializer, GYMListSerializer)
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
