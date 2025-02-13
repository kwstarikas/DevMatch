from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    class ProgrammingLanguage(models.TextChoices):
        CPP = "CPP", _("C++")
        JAVASCRIPT = "JS", _("Javascript")
        PYTHON = "PY", _("Python")
        JAVA = "JAVA", _("Java")
        LUA = "LUA", _("Lua")
        RUST = "RS", _("Rust")
        GO = "GO", _("Go")
        JULIA = "JL", _("Julia")

    class Level(models.TextChoices):
        BEGINNER = "BG", _("Begginer")
        EXPERIENCED = "EX", _("Experienced")
        EXPERT = "EP", _("Expert")

    level = models.CharField(max_length=2, choices=Level.choices)
    language = models.CharField(max_length=5, choices=ProgrammingLanguage.choices)

    def __str__(self):
        return f"Programming Language {self.language} with level {self.level}"


class Project(models.Model):
    class Level(models.TextChoices):
        RUNNING = "RN", _("Running")
        COMPLETED = "CP", _("Completed")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    project_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    maximum_collaborators = models.IntegerField()
    status = models.CharField(max_length=2)
    collaborators = models.ManyToManyField(
        User, related_name="collaborators", blank=True
    )
    open_positions = models.IntegerField()
    apllied_collaborators = models.ManyToManyField(
        User, related_name="apllied_collaborators", blank=True
    )

    def move_from_applied_to_collaborators(self, username):
        user = User.objects.get(username=username)
        if self.collaborators.count() < self.maximum_collaborators:
            self.collaborators.add(user)
            self.apllied_collaborators.remove(user)
            self.open_positions = (
                self.maximum_collaborators - self.collaborators.count()
            )

    def decline_applied_collaborators(self, username):
        user = User.objects.get(username=username)
        self.apllied_collaborators.remove(user)

    def get_applied_collaborator(self, username):
        return self.apllied_collaborators.get(username=username)

    def check_collaborator_exists(self, username):
        return self.apllied_collaborators.filter(username=username).exists

    def get_applied_collaborators(self):
        return self.apllied_collaborators.all()

    def __str__(self):
        return f"<{self.id}> Project {self.project_name}, owner: {self.owner.username} and status: {self.status}"


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    country = models.CharField(max_length=50, blank=True)
    skills = models.ManyToManyField(
        Skill, blank=True, related_name="dev_skills", related_query_name="dev_skill"
    )
    residence = models.CharField(max_length=50, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(age__gte=14),
                name="old_enough",
            ),
        ]
