from django.db import models

class Component(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=70)
    price = models.FloatField()
    description = models.TextField()
    technical_details = models.TextField()

class Pc(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_customized = models.BooleanField()
    components = models.ManyToManyField('Component', through='Pc_Components')

class Pc_Components(models.Model):
    pc = models.ForeignKey(Pc, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)

