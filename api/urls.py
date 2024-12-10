from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CompanyViewSet, DayViewSet, RegistrationRequestViewSet,
                    PaymentViewSet, WorkerViewSet, AdministratorViewSet, LeaveRequestViewSet)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'days', DayViewSet)
router.register(r'registration-requests', RegistrationRequestViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'administrators', AdministratorViewSet)
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')


urlpatterns = [
    path('', include(router.urls)),
]
