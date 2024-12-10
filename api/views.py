from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from api.models import Company, Day, RegistrationRequest, Payment, Worker, Administrator, LeaveRequest
from .serializers import (CompanySerializer, DaySerializer, RegistrationRequestSerializer,
                          PaymentSerializer, WorkerSerializer, AdministratorSerializer, LeaveRequestSerializer,
                          AdministratorLoginSerializer, WorkerRegistrationSerializer)

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

    def destroy(self, request, *args, **kwargs):
        try:
            worker = self.get_object()
            worker.delete()
            return Response(
                {"message": f"Сотрудник {worker.name} {worker.surname} успешно удален."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Worker.DoesNotExist:
            return Response(
                {"error": "Сотрудник не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
class AdministratorViewSet(ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer

class LeaveRequestViewSet(ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    @action(detail=True, methods=['post'])
    def approve_or_reject(self, request, pk=None):
        try:
            leave_request = self.get_object()  # Получаем объект LeaveRequest
            action_type = request.data.get('action')  # Тип действия: 'approve' или 'reject'

            if action_type not in ['approve', 'reject']:
                return Response(
                    {"error": "Некорректное действие. Используйте 'approve' или 'reject'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Меняем статус в зависимости от действия
            leave_request.status = 'approved' if action_type == 'approve' else 'rejected'
            leave_request.save()

            return Response(
                {"message": f"Запрос успешно {'одобрен' if action_type == 'approve' else 'отклонен'}."},
                status=status.HTTP_200_OK
            )

        except LeaveRequest.DoesNotExist:
            return Response(
                {"error": "Запрос не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class AdministratorLoginView(APIView):
    def post(self, request):
        serializer = AdministratorLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WorkerDetailsWithPayments(APIView):
    """
    API endpoint to retrieve worker details and associated payments.
    """

    def get(self, request, worker_id):
        try:
            worker = Worker.objects.get(pk=worker_id)
            worker_serializer = WorkerSerializer(worker)

            payments = Payment.objects.filter(employee_id=worker_id)
            payment_serializer = PaymentSerializer(payments, many=True)

            return Response({
                "worker": worker_serializer.data,
                "payments": payment_serializer.data
            })
        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=HTTP_404_NOT_FOUND)



class PaymentWorker(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['get'])
    def with_worker_info(self, request):
        try:
            payments = Payment.objects.select_related('employee')  # Используем select_related для оптимизации запросов
            payment_data = []

            for payment in payments:
                payment_info = {
                    'id': payment.id,
                    'amount': payment.amount,
                    'date': payment.date,
                    'worker': {
                        'id': payment.employee.id,
                        'name': payment.employee.name,
                        'surname': payment.employee.surname,
                        'position': payment.employee.position,
                        'salary': payment.employee.salary,
                    }
                }
                payment_data.append(payment_info)

            return Response(payment_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Произошла ошибка: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class WorkerRegistrationView(APIView):
    def post(self, request):
        serializer = WorkerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)