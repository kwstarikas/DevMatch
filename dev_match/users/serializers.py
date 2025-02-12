import pprint

from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import Developer, Skill

pp = pprint.PrettyPrinter(indent=4)


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ["level", "language"]


class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source="developer.age")
    country = serializers.CharField(source="developer.country")
    residence = serializers.CharField(source="developer.residence")
    available_skills = SkillSerializer(source="developer.skills", many=True)

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
            "available_skills",
        ]


class ProgrammingLanguageSerializer(serializers.Serializer):
    level = serializers.CharField(required=False)
    name = serializers.CharField()

    class Meta:
        fields = ["name", "level"]


class CreateUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source="developer.age")
    country = serializers.CharField(source="developer.country")
    residence = serializers.CharField(source="developer.residence")

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
        ]
        extra_kwargs = {
            "id": {"read_only": True},
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
            Developer.objects.create(user=user, **developer_data)
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


class AddSkillSerializer(serializers.ModelSerializer):
    skills = SkillSerializer()

    class Meta:
        model = User
        fields = ["skills"]

    def validate(self, attrs):
        user_id = self.context.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
            dev = Developer.objects.get(user=user)
        except:
            raise serializers.ValidationError("User ID is invalid")

        if dev.skills.all().count() >= 3:
            raise serializers.ValidationError(
                "You already have 3 skills, if you want to add, delete one first"
            )
        if dev.skills.filter(language=attrs["skills"]["language"]).exists():
            raise serializers.ValidationError("language of this skill already exists")

        print("AVAILABLE OPTIONS : \n", dict(Skill.ProgrammingLanguage.choices))
        return attrs

    def create(self, validated_data):
        user_id = self.context.get("user_id")

        with transaction.atomic():
            skill_to_add = Skill.objects.get_or_create(
                level=validated_data["skills"]["level"],
                language=validated_data["skills"]["language"],
            )
            user = User.objects.get(pk=user_id)
            dev = Developer.objects.get(user=user)
            dev.skills.add(Skill.objects.get(id=skill_to_add[0].id))
            dev.save()
        return validated_data


class RemoveSkillSerializer(AddSkillSerializer):
    class Meta:
        model = User
        fields = AddSkillSerializer.Meta.fields

    def validate(self, attrs):
        print("YELLO")
        user_id = self.context.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
            dev = Developer.objects.get(user=user)
        except:
            raise serializers.ValidationError("User ID is invalid")

        try:
            exist = dev.skills.filter(language=attrs["skills"]["language"]).first()
            print(exist)
        except Exception as e:
            print(e)
            raise serializers.ValidationError("User does not have this skill")
        return attrs

    def create(self, validated_data):
        user_id = self.context.get("user_id")

        user = User.objects.get(pk=user_id)
        dev = Developer.objects.get(user=user)
        dev.skills.remove(
            Skill.objects.get(
                level=validated_data["skills"]["level"],
                language=validated_data["skills"]["language"],
            )
        )
        dev.save()
        return validated_data
