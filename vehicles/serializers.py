from rest_framework import serializers
from .models import Component, Vehicle, Issue, Payment

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ("name",)

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("name",)


# class IssueSerializer(serializers.ModelSerializer):
#     component = ComponentSerializer(many=True)
#     vehicle = VehicleSerializer(read_only=True)  # Not many=True, since it's a single vehicle

#     class Meta:
#         model = Issue
#         fields = ("vehicle", "component", "description", "is_repair", "is_purchased")

class IssueSerializer(serializers.ModelSerializer):
    component= ComponentSerializer(many=True)
    vehicle= VehicleSerializer()

    class Meta:

        model = Issue
        fields =("vehicle","component","description","is_repair","is_purchased")

        # def to_representation(self, instance):
        #     vehicle_data = VehicleSerializer(instance.vehicle).data
        #     return {
        #         'id': instance.id,
        #         'vehicle': vehicle_data,
        #         # Other fields
        #     }
        def to_representation(self, instance):
            
        # Serialize vehicle and components
            vehicle_data = VehicleSerializer(instance.vehicle).data if instance.vehicle else None

            component_data = ComponentSerializer(instance.component.all(), many=True).data
            print(instance.vehicle)
              # Use .all() to get all related components

            return {
                'id': instance.id,
                'vehicle': vehicle_data,
                'component': component_data,  # List of serialized components
                'description': instance.description,
                'is_repair': instance.is_repair,
                'is_purchased': instance.is_purchased,
            }

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

