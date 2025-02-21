from enum import unique

from django.db import models
from psycopg2 import DATETIME


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    pcs = models.ManyToManyField('pc_components.Pc', through='User_Pc')

    def __str__(self):
        return self.username


class User_Pc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pc = models.ForeignKey('pc_components.Pc', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.pc.id}"







