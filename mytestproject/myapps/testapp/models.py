from django.db import models

# Create your models here.


class testdb(models.Model):
    col1 = models.CharField(max_length=10)
    col2 = models.IntegerField()
