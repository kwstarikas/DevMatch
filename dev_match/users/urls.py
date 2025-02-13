from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views.user_views import UserViewSet
from .views.project_views import ProjectViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"projects", ProjectViewSet, basename="projects")

urlpatterns = [path("", include(router.urls))]
