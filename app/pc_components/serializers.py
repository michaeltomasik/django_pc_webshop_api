from rest_framework import serializers
from models import Component, Pc

class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = '__all__'


class PcSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Pc
        fields = '__all__'

