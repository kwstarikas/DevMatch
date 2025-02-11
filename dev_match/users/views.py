from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import mixins
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .serializers import UserSerializer, CreateUserSerializer, UserLoginSerializer
import pprint
from rest_framework.authtoken.models import Token

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
    login=extend_schema(
        summary="Login a User",
        description="blah blah blah",
    ),
)
class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    http_method_names = ["post", "get", "patch"]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateUserSerializer
        elif self.action in ["login"]:
            return UserLoginSerializer
        return UserSerializer

    def get_permissions(self):
        print("IN permisions class", self.action)
        if self.action in ["list"]:
            print("GOT IN GET")
            return [permissions.IsAuthenticated()]
        return []

    def list(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return super().list(request, *args, **kwargs)
