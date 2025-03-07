from rest_framework import serializers
from .models import Order, Order_Item


class OrderSerializer(serializers.ModelSerializer):
    #user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Order
        #fields = '__all__'
        exclude = ['user']

class Order_ItemSerializer(serializers.ModelSerializer):
    pc_id = serializers.StringRelatedField()
    component_id = serializers.StringRelatedField()

    class Meta:
        model = Order_Item
        fields = '__all__'

    def validate_pc(self, value):
        if self.initial_data.get('order_type') == 'pc' and self.initial_data.get('component') is None:
            raise serializers.ValidationError("Component must be specified for 'pc' type order.")
        return value

    def validate_component(self, value):
        if self.initial_data.get('order_type') == 'component' and self.initial_data.get('pc') is None:
            raise serializers.ValidationError("Component must be specified for 'pc' type order.")
        return value