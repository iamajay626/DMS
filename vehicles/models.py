from django.db import models
from decimal import Decimal

class Component(models.Model):
    name = models.CharField(max_length=100)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_price= models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.name}"

class Issue(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='issues', on_delete=models.CASCADE)
    component = models.ManyToManyField(Component)
    description = models.TextField(max_length=200)
    is_repair = models.BooleanField(default=False)
    is_purchased=models.BooleanField(default=False)


    def calculate_price(self):
        if self.is_repair:
            return self.component.repair_price
        elif self.is_purchased:
            return self.component.repair_price + self.component.purchase_price


    def __str__(self):
        return f"Issue for {self.vehicle.name}"

class Payment(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.vehicle.name} - {self.amount}"

