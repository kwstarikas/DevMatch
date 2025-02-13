from rest_framework import status
from rest_framework import mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter


from ..models import Project
from ..serializers.project_serializers import (
    ProjectSerializer,
    ApplyToProjectSerializer,
    AcceptContriburtor,
    DeclineContriburtor,
)


@extend_schema(tags=["Projects"])
@extend_schema_view(
    list=extend_schema(
        summary="Retrieve all projects",
        description="blah blah blah",
    ),
    destroy=extend_schema(
        summary="Retrieve all projects",
        description="blah blah blah",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="user_id of the project's owner",
                type=int,
            ),
        ],
    ),
    apply_to_project=extend_schema(
        summary="Create a Project",
        description="blah blah blah",
        parameters=[
            OpenApiParameter(
                name="username",
                description="username of user who wants to apply",
                type=str,
            ),
        ],
    ),
    accept_contributor=extend_schema(
        summary="Accept contributor a Project",
        description="blah blah blah",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="user_id of the project's owner",
                type=int,
            ),
        ],
    ),
    decline_contributor=extend_schema(
        summary="Decline contributor a Project",
        description="blah blah blah",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="user_id of the project's owner",
                type=int,
            ),
        ],
    ),
    set_project_complete=extend_schema(
        summary="set project status to complete",
        description="blah blah blah",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="user_id of the project's owner",
                type=int,
            ),
        ],
        request=ApplyToProjectSerializer,
    ),
)
class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    http_method_names = ["post", "get", "patch", "delete"]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.action in ["get_available_projects"]:
            return Project.objects.filter(open_positions__gt=0, status="RN")
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action in ["apply_to_project"]:
            return ApplyToProjectSerializer
        elif self.action in ["accept_contributor"]:
            return AcceptContriburtor
        elif self.action in ["decline_contributor"]:
            return DeclineContriburtor
        return ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        project = self.get_object()
        if not User.objects.filter(id=user_id).exists():
            return Response(
                data={"User does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if str(project.owner.id) != str(user_id):
            return Response(
                data={"User trying to delete project where its not owner"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["patch"],
        name="set-project-complete",
        url_path="set-project-complete",
        url_name="set-project-complete",
    )
    def set_project_complete(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        project = self.get_object()
        if not User.objects.filter(id=user_id).exists():
            return Response(
                data={"User does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if str(project.owner.id) != str(user_id):
            return Response(
                data={"User trying to delete project where its not owner"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        project.status = "CP"
        project.save()
        return Response(data={"Project's status changed"}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["Get"],
        name="get-available-projects",
        url_path="get-available-projects",
        url_name="get-available-projects",
    )
    def get_available_projects(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["patch"],
        name="aplly-to-project",
        url_path="aplly-to-project",
        url_name="aplly-to-project",
    )
    def apply_to_project(self, request, *args, **kwargs):
        project = self.get_object()
        username = self.request.query_params.get("username")

        serializer = self.get_serializer(
            data=request.data, instance=project, context={"username": username}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        name="accept-contributor",
        url_path="accept-contributor",
        url_name="accept-contributor",
    )
    def accept_contributor(self, request, *args, **kwargs):
        project = self.get_object()
        user_id = self.request.query_params.get("user_id")

        serializer = self.get_serializer(
            data=request.data, instance=project, context={"user_id": str(user_id)}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        name="decline-contributor",
        url_path="decline-contributor",
        url_name="decline-contributor",
    )
    def decline_contributor(self, request, *args, **kwargs):
        project = self.get_object()
        user_id = self.request.query_params.get("user_id")

        serializer = self.get_serializer(
            data=request.data, instance=project, context={"user_id": str(user_id)}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
