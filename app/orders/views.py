from rest_framework import viewsets
from models import Order, Order_Item
from serializers import OrderSerializer, Order_ItemSerializer
from rest_framework.permissions import IsAuthenticated
from ..users.permissions import IsOwner


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    ordering = ['created_at']


class Order_ItemViewSet(viewsets.ModelViewSet):
    queryset = Order_Item.objects.all()
    serializer_class = Order_ItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    ordering = ['id']