from django.db import models


class Cms (models.Model):
	clave = models.CharField (max_length=32)
	contenido = models.CharField (max_length=200)

# Create your models here.
