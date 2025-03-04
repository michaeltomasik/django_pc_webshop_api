from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    total_price = models.FloatField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)

    def __str__(self):
        return self.id

class Order_Item(models.Model):
    ORDER_TYPE_CHOICES = [
        ('pc', 'PC'),
        ('component', 'Component'),
    ]
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pc = models.ForeignKey('pc_components.Pc', blank=True, null=True, on_delete=models.CASCADE)
    component = models.ForeignKey('pc_components.Component', blank=True, null=True, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=9, choices=ORDER_TYPE_CHOICES)
    quantity = models.IntegerField()

    def __str__(self):
        if self.order_type == 'pc':
            return f"PC: {self.pc.name} - Quantity: {self.quantity}"
        elif self.order_type == 'component':
            return f"Component: {self.component.name} - Quantity: {self.quantity}"






