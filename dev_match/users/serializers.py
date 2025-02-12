import pprint

from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import Developer

pp = pprint.PrettyPrinter(indent=4)


class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source="developer.age")
    country = serializers.CharField(source="developer.country")
    residence = serializers.CharField(source="developer.residence")
    programming_languages = serializers.SerializerMethodField(
        "get_programming_languages"
    )

    def get_programming_languages(self, obj):
        return obj.developer.programming_languages

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "country",
            "residence",
            "programming_languages",
        ]


class ProgrammingLanguageSerializer(serializers.Serializer):
    level = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        fields = ["name", "level"]


class CreateUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source="developer.age")
    country = serializers.CharField(source="developer.country")
    residence = serializers.CharField(source="developer.residence")
    programming_languages = serializers.ListField(
        source="developer.programming_languages", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "age",
            "country",
            "residence",
            "programming_languages",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "programming_languages": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_age(self, value):
        if value < 14:
            raise serializers.ValidationError("Too young to join the platform")
        return value

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"].lower()):
            raise serializers.ValidationError("This email address already exists")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            developer_data = validated_data.pop("developer")
            user = User.objects.create(**validated_data)
            Developer.objects.create(**developer_data, user=user)
            return user
        raise serializers.ValidationError(
            "Error While creating the User, plz try again xd "
        )


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        field = ["password"]

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("token", None)
        user_id = self.context.get("user_id", None)

        if token is None or user_id is None:
            raise serializers.ValidationError("Error invalid url")

        try:
            user = User.objects.get(pk=user_id)
        except:
            raise serializers.ValidationError("User ID is invalid")
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
