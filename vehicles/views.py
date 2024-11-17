from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Component, Vehicle, Issue, Payment
from .serializers import ComponentSerializer, VehicleSerializer, IssueSerializer, PaymentSerializer
from rest_framework.decorators import api_view
from django.db.models import Sum
from datetime import datetime


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class IssueViewSet(viewsets.ModelViewSet):
    # queryset = Issue.objects.prefetch_related('component').select_related('vehicle')
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            print(valid_data)

            # {'vehicle': {'name': 'bens'}, 'component': [{'name': 'mirror'}], 'description': 'test', 'is_repair': False, 'is_purchased': True}
            
            # Assuming 'vehicle' is a ForeignKey, handle it accordingly
            vehicle_name = valid_data['vehicle']['name']
            
            component_names = [comp['name'] for comp in valid_data['component']]
            description = data['description']
            is_repair = data['is_repair']
            is_purchased = data['is_purchased']

            vehicle_obj=Vehicle.objects.get(name=vehicle_name)
            comp_obj_list=[]
            for comp in component_names:
                comp_ojb=Component.objects.get(name=comp)
                comp_obj_list.append(comp_ojb)
            print(vehicle_obj)
            print(comp_obj_list)
            issue = Issue.objects.create(
            vehicle=vehicle_obj,
            description=description,
            is_repair=is_repair,
            is_purchased=is_purchased)
            issue.component.set(comp_obj_list) 


            print(vehicle_name)
            print(component_names)
            print(description)
            print(is_repair)
            print(is_purchased)




            # if vehicle_name:
            #     # If vehicle is passed as an ID, fetch the corresponding Vehicle instance
            #     if isinstance(vehicle, dict):  # If vehicle is a nested object
            #         vehicle_instance = Vehicle.objects.get(id=vehicle.get('id'))
            #         valid_data['vehicle'] = vehicle_instance
            #     # If it's already a single Vehicle instance, no need to fetch it
            # Issue.objects.create(**valid_data)

            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class IssueViewSet(viewsets.ModelViewSet):
#     queryset = Issue.objects.all()
#     serializer_class = IssueSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.get_serializer(data=data)
#         if serializer.is_valid():
#             valid_data = serializer.validated_data
#             print(valid_data)

#             # Ensure you're handling related fields (like 'vehicle') properly
#             vehicle = valid_data.get('vehicle')  # If 'vehicle' is a ForeignKey
#             if vehicle:
#                 # Check if 'vehicle' is an actual Vehicle instance or just an ID
#                 if isinstance(vehicle, Vehicle):
#                     # Correctly handle if the vehicle is passed as an object
#                     Issue.objects.create(vehicle=vehicle, **valid_data)
#                 else:
#                     # If it's just an ID, fetch the actual Vehicle object
#                     Issue.objects.create(vehicle_id=vehicle, **valid_data)
#             else:
#                 # Handle case where no vehicle is provided (if applicable)
#                 Issue.objects.create(**valid_data)
            
#             return Response(request.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class IssueViewSet(viewsets.ModelViewSet):
#     queryset = Issue.objects.all()
#     serializer_class = IssueSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializer=self.get_serializer(data=data)
#         if serializer.is_valid():
#             valid_data=serializer.validated_data
#             print(valid_data)
#             Issue.objects.create(**valid_data)

#             # component = Component.objects.get(id=data["component"])
#             # is_repair = data.get("is_repair", False)
#             # print(type(is_repair))
#             # print(is_repair)  # Check if it's for repair
#             # issue = Issue.objects.create(
#             #     vehicle_id=data["vehicle"],
#             #         component=component,
#             #     description=data["description"],
#             #     is_repair=is_repair
#         # )
#         return Response(request.data, status=status.HTTP_201_CREATED)
    


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        vehicle = Vehicle.objects.get(id=data["vehicle"])
        issues = Issue.objects.filter(vehicle=vehicle)
        if sum([issue.calculate_price() for issue in issues]):
            total_amount=sum([issue.calculate_price() for issue in issues])
        else:
            total_amount=amount
        print(total_amount)
        
        payment = Payment.objects.create(
            vehicle=vehicle,
            amount=total_amount
        )
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def revenue_report(request):
    today = datetime.today().date()
    daily_revenue = Payment.objects.filter(date=today).aggregate(total=Sum('amount'))
    monthly_revenue = Payment.objects.filter(date__month=today.month).aggregate(total=Sum('amount'))
    yearly_revenue = Payment.objects.filter(date__year=today.year).aggregate(total=Sum('amount'))
    return Response({
        "daily_revenue": daily_revenue["total"] if daily_revenue["total"] else 0,
        "monthly_revenue": monthly_revenue["total"] if monthly_revenue["total"] else 0,
        "yearly_revenue": yearly_revenue["total"] if yearly_revenue["total"] else 0,
    })

