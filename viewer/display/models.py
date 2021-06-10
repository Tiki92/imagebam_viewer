from django.db import models
from django.utils.timezone import now


class Links(models.Model):
    link = models.CharField(max_length=200)
    checked_date = models.DateTimeField(editable=False, auto_now=True)
    img_tag = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(default=200)


class Galleries(models.Model):
    link = models.CharField(max_length=200)
    gallery_link = models.CharField(max_length=200)
    checked_date = models.DateTimeField(editable=False, auto_now=True)
    img_tag = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(default=200)


class Patterns(models.Model):
    pattern = models.CharField(max_length=200)


class CurrentPattern(models.Model):
    current = models.IntegerField()


class LastViewedImage(models.Model):
    current = models.IntegerField(default=1)
    page = models.IntegerField(default=1)


class LastViewedGallerie(models.Model):
    current = models.IntegerField(default=1)
    page = models.IntegerField(default=1)
