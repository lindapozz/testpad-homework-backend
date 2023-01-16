from django.db import models

# Create your models here.

class Url(models.Model):
    url =  models.TextField()
    result = models.IntegerField()

    def _str_(self):
        return self.url