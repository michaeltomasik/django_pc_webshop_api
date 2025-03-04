from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet, Order_ItemViewSet

order_router = DefaultRouter()
order_router.register('orders', OrderViewSet)

order_item_router = DefaultRouter()
order_item_router.register('order_items', Order_ItemViewSet)


urlpatterns = [
    path('', include(order_router.urls)),
    path('', include(order_item_router.urls)),
]
