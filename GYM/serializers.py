from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import GYM, Type, Classes, Booking


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
            payload = RefreshToken.for_user(user_obj)
            token = str(payload.access_token)
            data["access"] = token
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError(
                "Incorrect username/password combination! Noob..")

        return data


class GYMListSerializer(serializers.ModelSerializer):  # GYM list
    class Meta:
        model = GYM
        fields = ['id', 'name', 'number_of_classes', 'location']


class ClassesListSerializer(serializers.ModelSerializer):  # classes list

    gym = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='name'
    )
    type_of = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Classes
        fields = ['gym', 'type_of', 'id', 'name',
                  'limits', 'start', 'price', 'img']


class ClassesDetailSerializer(serializers.ModelSerializer):  # classes list

    gym = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='name'
    )
    type_of = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Classes
        fields = ['gym', 'type_of', 'id', 'name', 'limits',
                  'description', 'start', 'end', 'price', 'img']


class GYMCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GYM
        fields = ['name', 'number_of_classes', 'location']


class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['name', 'limits',
                  'description', 'start', 'end', 'price', 'img']


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['customer', 'class_of', 'time']


class BookingListSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='username'
    )
    class_of = serializers.SlugRelatedField(
        many=False,  # it's by Default
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'class_of', 'time']
