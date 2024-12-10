from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CompanyViewSet, DayViewSet, RegistrationRequestViewSet,
                    PaymentViewSet, WorkerViewSet, AdministratorViewSet, LeaveRequestViewSet, AdministratorLoginView,
                    WorkerDetailsWithPayments)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', AdministratorLoginView.as_view(), name='administrator_login'),
    path('worker/<int:worker_id>/details-with-payments/', WorkerDetailsWithPayments.as_view(),
         name='worker_details_with_payments'),
]
