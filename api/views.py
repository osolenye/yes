from rest_framework.viewsets import ModelViewSet
from api.models import Company, Day, RegistrationRequest, Payment, Worker, Administrator
from .serializers import CompanySerializer, DaySerializer, RegistrationRequestSerializer, PaymentSerializer, WorkerSerializer, AdministratorSerializer

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DayViewSet(ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class RegistrationRequestViewSet(ModelViewSet):
    queryset = RegistrationRequest.objects.all()
    serializer_class = RegistrationRequestSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
class AdministratorViewSet(ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
