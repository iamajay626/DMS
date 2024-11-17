from django.contrib import admin
from . models import Component,Vehicle,Issue,Payment,Decimal

# Register your models here.
admin.site.register(Component)
admin.site.register(Vehicle)
admin.site.register(Issue)
admin.site.register(Payment)