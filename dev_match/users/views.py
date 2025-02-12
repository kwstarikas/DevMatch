import pprint

from rest_framework import status
from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    PasswordResetSerializer,
    RequestPasswordResetSerializer,
)

pp = pprint.PrettyPrinter(indent=4)


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
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateUserSerializer
        elif self.action in ["request_reset_password"]:
            return RequestPasswordResetSerializer
        elif self.action in ["reset_password"]:
            return PasswordResetSerializer
        return UserSerializer

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
