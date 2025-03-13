from rest_framework import viewsets
from .models import Order, Order_Item
from .serializers import OrderSerializer, Order_ItemSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOrderOwner, IsOrder_Item_Owner


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user_id=self.request.user.id)


class Order_ItemViewSet(viewsets.ModelViewSet):
    queryset = Order_Item.objects.all()
    serializer_class = Order_ItemSerializer
    permission_classes = [IsAuthenticated, IsOrder_Item_Owner]
    ordering = ['id']