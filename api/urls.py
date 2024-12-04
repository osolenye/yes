from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, DayViewSet, RegistrationRequestViewSet, PaymentViewSet, WorkerViewSet, AdministratorViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'days', DayViewSet)
router.register(r'registration-requests', RegistrationRequestViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'workers', WorkerViewSet, basename='worker')  # Указываем basename
router.register(r'administrators', AdministratorViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
