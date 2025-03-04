from rest_framework import serializers
from models import Order, Order_Item

class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = '__all__'

class Order_ItemSerializer(serializers.ModelSerializer):
    pc_id = serializers.StringRelatedField()
    component_id = serializers.StringRelatedField()

    class Meta:
        model = Order_Item
        fields = '__all__'

    def validate_pc(self, value):
        """Check if component_id is not used when pc_id is used"""
        if self.initial_data.get('order_type') == 'pc' and self.initial_data.get('component') is None:
            raise serializers.ValidationError("Component must be specified for 'pc' type order.")
        return value

    def validate_component(self, value):
        """Check if pc_id is not used when component_id is used"""
        if self.initial_data.get('order_type') == 'component' and self.initial_data.get('pc') is None:
            raise serializers.ValidationError("Component must be specified for 'pc' type order.")
        return value