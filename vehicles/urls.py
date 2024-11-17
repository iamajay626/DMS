from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, VehicleViewSet, IssueViewSet, PaymentViewSet, revenue_report

router = DefaultRouter()
router.register("components", ComponentViewSet)
router.register("vehicles", VehicleViewSet)
router.register("issues", IssueViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("revenue_report/", revenue_report, name="revenue_report"),
]
