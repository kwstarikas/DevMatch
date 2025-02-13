from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Developer, Project
from .user_serializers import SkillSerializer


class CollaboratorsSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(source="developer.skills", many=True)
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = Developer
        fields = [
            "username",
            "email",
            "skills",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorsSerializer(many=True, read_only=True)
    apllied_collaborators = CollaboratorsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "owner",
            "project_name",
            "description",
            "maximum_collaborators",
            "status",
            "open_positions",
            "collaborators",
            "apllied_collaborators",
        ]


class CreateProjectSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "owner",
            "project_name",
            "description",
            "maximum_collaborators",
            "status",
            "open_positions",
            "collaborators",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "status": {"read_only": True},
            "open_positions": {"read_only": True},
        }

    def validate(self, attrs):
        print("In validate")
        return attrs

    def create(self, validated_data):
        print("In create")
        user = self.context.get("user")
        validated_data["status"] = "RN"
        validated_data["open_positions"] = validated_data["maximum_collaborators"]
        Project.objects.create(**validated_data, owner=user)
        return validated_data


class ApplyToProjectSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "project_name",
            "collaborators",
            "open_positions",
            "maximum_collaborators",
        ]
        extra_kwargs = {
            "project_name": {"read_only": True},
            "open_positions": {"read_only": True},
            "maximum_collaborators": {"read_only": True},
        }

    def validate(self, attrs):
        print("in Validate")
        username = self.context.get("username")
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f"Invalid username {username} does not exist"
            )

        if not self.instance.open_positions > 0:
            raise serializers.ValidationError(
                f"This project {self.instance} does not have open positions "
            )
        if self.instance.status != "RN":
            raise serializers.ValidationError(
                f"This project {self.instance} is not running so it doesnt accept any more contributions"
            )
        return attrs

    def update(self, instance, validated_data):
        instance.apllied_collaborators.add(
            User.objects.get(username=self.context.get("username"))
        )

        return instance


class AcceptContriburtor(ApplyToProjectSerializer):
    username = serializers.CharField()

    class Meta:
        model = Project
        fields = ApplyToProjectSerializer.Meta.fields + ["username"]
        extra_kwargs = {
            "project_name": {"read_only": True},
            "open_positions": {"read_only": True},
            "maximum_collaborators": {"read_only": True},
        }

    def validate(self, attrs):
        user_id = self.context.get("user_id")
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError(
                f"Invalid user with id  {user_id} does not exist"
            )

        if str(self.instance.owner.id) != user_id:
            raise serializers.ValidationError(
                "You dont have permision do accept in project you are not owner"
            )
        if not self.instance.check_collaborator_exists(attrs["username"]):
            raise serializers.ValidationError(
                "invalid username, does not exist in applied collaborators"
            )
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.move_from_applied_to_collaborators(validated_data["username"])
            instance.save()

        return validated_data


class DeclineContriburtor(ApplyToProjectSerializer):
    username = serializers.CharField()

    class Meta:
        model = Project
        fields = ApplyToProjectSerializer.Meta.fields + ["username"]
        extra_kwargs = {
            "project_name": {"read_only": True},
            "open_positions": {"read_only": True},
            "maximum_collaborators": {"read_only": True},
        }

    def validate(self, attrs):
        user_id = self.context.get("user_id")
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError(
                f"Invalid user with id  {user_id} does not exist"
            )

        if str(self.instance.owner.id) != user_id:
            raise serializers.ValidationError(
                "You dont have permision do decline in project you are not owner"
            )
        if not self.instance.check_collaborator_exists(attrs["username"]):
            raise serializers.ValidationError(
                "invalid username, does not exist in applied collaborators"
            )
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.decline_applied_collaborators(validated_data["username"])
            instance.save()

        return validated_data
