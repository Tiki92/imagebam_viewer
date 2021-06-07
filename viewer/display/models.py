from django.db import models
from django.utils.timezone import now


class Links(models.Model):
    link = models.CharField(max_length=200)
    checked_date = models.DateTimeField(editable=False, auto_now=True)
    img_tag = models.CharField(max_length=500, blank=True)

class Galleries(models.Model):
    link = models.CharField(max_length=200)
    gallery_link = models.CharField(max_length=200)
    checked_date = models.DateTimeField(editable=False, auto_now=True)
    img_tag = models.CharField(max_length=500, blank=True)

class Patterns(models.Model):
    pattern = models.CharField(max_length=200)

class CurrentPattern(models.Model):
    current = models.IntegerField()