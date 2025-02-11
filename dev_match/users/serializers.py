from rest_framework import serializers
from django.contrib.auth.models import User
import pprint
from django.core.validators import validate_email
from .models import Developer
from django.db import transaction

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
        source="developer.programming_languages"
    )
    # programming_languages = ProgrammingLanguageSerializer(many=True)

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
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def validate(self, attrs):
        print("IN VAL WUITH ", attrs)
        if User.objects.filter(email=attrs["email"].lower()):
            raise serializers.ValidationError("This email address already exists")

        return attrs

    def create(self, validated_data):

        with transaction.atomic():

            pp.pprint(validated_data)
            developer_data = validated_data.pop("developer")
            pp.pprint(developer_data)
            user = User.objects.create(**validated_data)
            Developer.objects.create(**developer_data, user=user)
            return user
        raise serializers.ValidationError("Error in create")


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        return attrs
