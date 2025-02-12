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
