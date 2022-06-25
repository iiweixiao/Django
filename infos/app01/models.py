from django.db import models


class SougouNewsInfo(models.Model):
    title = models.CharField(max_length=100)
    href = models.CharField(max_length=150)
    source = models.CharField(max_length=20)
    created = models.CharField(max_length=15)
