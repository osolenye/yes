from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Company, Day, RegistrationRequest, Payment, Worker, Administrator, LeaveRequest, CustomUser


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'


class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = '__all__'


# class PaymentSerializer(serializers.ModelSerializer):
#     worker = WorkerSerializer(read_only=True)
#     class Meta:
#         model = Payment
#         fields = '__all__'
#
# class WorkerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Worker
#         fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        # fields = ('id', 'name', 'surname')  # Customize the fields as needed
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        # fields = ('id', 'amount', 'date', 'worker')


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

        def validate(self, data):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("Дата окончания не может быть раньше даты начала.")
            return data


class AdministratorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            admin = Administrator.objects.get(name=data['username'])
            if admin.password != data['password']:  # Для простоты сравниваем пароли без хеширования
                raise serializers.ValidationError("Неверный пароль.")
        except Administrator.DoesNotExist:
            raise serializers.ValidationError("Администратор с таким именем не найден.")

        refresh = RefreshToken.for_user(admin)
        return {
            'id': admin.id,  # Add the admin's ID to the response
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class WorkerRegistrationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Worker
        fields = ('name', 'surname', 'salary', 'phone_number', 'position', 'company', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
        worker = Worker.objects.create(user=user, **validated_data)
        return worker