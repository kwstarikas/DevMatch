from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from enumchoicefield import EnumChoiceField

from enum import Enum


class ProgrammingLanguage(Enum):
    CPP = "CPP"
    JAVASCRIPT = "JS"
    PYTHON = "PY"
    JAVA = "JAVA"
    LUA = "LUA"
    RUST = "RS"
    GO = "GO"
    JULIA = "JL"


def programming_language_dict():
    return {"skills": []}


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(14)]
    )
    country = models.CharField(max_length=50)
    programming_languages = models.JSONField(default=programming_language_dict)
    residence = models.CharField(max_length=50)
