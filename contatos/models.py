from django.db import models
from django.utils import timezone


class Contato(models.Model):
    email = models.CharField(max_length=255)
    data_nascimento = models.DateTimeField(default=timezone.now)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.email
