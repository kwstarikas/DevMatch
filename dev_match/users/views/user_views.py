from rest_framework import status
from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from ..models import Project, Skill
from ..serializers.user_serializers import (
    UserSerializer,
    AddSkillSerializer,
    CreateUserSerializer,
    RemoveSkillSerializer,
    PasswordResetSerializer,
    RequestPasswordResetSerializer,
)
from ..serializers.project_serializers import CreateProjectSerializer, ProjectSerializer


@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(
        summary="Retrieve all users",
        description="blah blah blah",
    ),
    create=extend_schema(
        summary="Create a User",
        description="blah blah blah",
    ),
    update=extend_schema(
        summary="Update a User",
        description="blah blah blah",
    ),
    request_reset_password=extend_schema(
        summary="request reset password",
        description="blah blah blah",
    ),
    reset_password=extend_schema(
        summary="request reset password",
        description="blah blah blah",
        parameters=[
            OpenApiParameter(name="token", description="Category Id", type=str),
            OpenApiParameter(name="user_id", description="Category Id", type=str),
        ],
    ),
    add_skill=extend_schema(
        summary="request reset password",
        description="blah blah blah",
    ),
    statistics=extend_schema(
        summary="request reset password",
        description="blah blah blah",
    ),
)
class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    http_method_names = ["post", "get", "patch"]
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateUserSerializer
        elif self.action in ["request_reset_password"]:
            return RequestPasswordResetSerializer
        elif self.action in ["reset_password"]:
            return PasswordResetSerializer
        elif self.action in ["add_skill"]:
            return AddSkillSerializer
        elif self.action in ["remove_skill"]:
            return RemoveSkillSerializer
        elif self.action in ["create_project"]:
            return CreateProjectSerializer
        elif self.action in ["get_available_projects"]:
            return ProjectSerializer

        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["patch"],
        name="reset-password",
        url_path="reset-password",
        url_name="reset-password",
    )
    def reset_password(self, request, *args, **kwargs):
        token = self.request.query_params.get("token")
        user_id = self.request.query_params.get("user_id")

        serializer = self.get_serializer(
            data=request.data, context={"token": token, "user_id": user_id}
        )
        serializer.is_valid(raise_exception=True)

        return Response(data={}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["patch"],
        name="request-reset-password",
        url_path="request-reset-password",
        url_name="request-reset-password",
    )
    def request_reset_password(self, request, *args, **kwargs):
        try:
            # check if user exists
            user = User.objects.get(email=request.data.get("email"))
        except:
            return Response(
                data="User with email : {} does not exist".format(
                    request.data.get("email")
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = user.id

        token = PasswordResetTokenGenerator().make_token(user)

        reset_url = (
            f"127.0.0.1:8000/users/reset-password/?user_id={user_id}&token={token}/"
        )

        # send the rest_link as mail to the user.

        return Response(
            data={"message": f"Your password rest link: {reset_url}"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["patch"],
        name="add-skill",
        url_path="add-skill",
        url_name="add-skill",
    )
    def add_skill(self, request, *args, **kwargs):
        user_instance = self.get_object()

        serializer = self.get_serializer(data=request.data, instance=user_instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        name="remove-skill",
        url_path="remove-skill",
        url_name="remove-skill",
    )
    def remove_skill(self, request, *args, **kwargs):
        user_instance = self.get_object()

        serializer = self.get_serializer(data=request.data, instance=user_instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={"message": "Skill removed"}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        name="create-project",
        url_path="create-project",
        url_name="create-project",
    )
    def create_project(self, request, *args, **kwargs):
        user_instance = self.get_object()

        serializer = self.get_serializer(
            data=request.data, context={"user": user_instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["get"],
        name="statistics",
        url_path="statistics",
        url_name="statistics",
    )
    def statistics(self, request, *args, **kwargs):
        users = User.objects.all()
        data = {}
        for user in users:
            data[user.id] = {
                "owned projects": user.developer.get_projects_owned(),
                "projects Contributed": user.developer.get_projects_contributed(),
            }
        data["most used language"] = Skill.get_most_used_language()
        data["most used level"] = Skill.get_most_used_level()
        return Response(data=data, status=status.HTTP_200_OK)
