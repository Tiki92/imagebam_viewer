from django.db import models


class Links(models.Model):
    link = models.CharField(max_length=200)
    checked_date = models.DateTimeField("date checked")
