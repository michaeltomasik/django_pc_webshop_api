from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    total_price = models.FloatField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)

class Order_Item(models.Model):
    ORDER_TYPE_CHOICES = [
        ('pc', 'PC'),
        ('component', 'Component'),
    ]

    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    pc_id = models.ForeignKey('pc_components.Pc', blank=True, null=True, on_delete=models.CASCADE)
    component_id = models.ForeignKey('pc_components.Component', blank=True, null=True, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=9, choices=ORDER_TYPE_CHOICES)
    quantity = models.IntegerField()







