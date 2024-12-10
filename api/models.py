from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    number_of_employees = models.IntegerField()

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    # ... other fields

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",  # Add related_name here
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Add related_name here
    )


class Worker(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    salary = models.FloatField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, default=None)


    def __str__(self):
        return f"{self.name} {self.surname}"


class Administrator(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Day(models.Model):
    span = models.CharField(max_length=255)  # e.g., "09:00-17:00"
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)


class RegistrationRequest(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Worker, on_delete=models.CASCADE)
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)


class Payment(models.Model):
    amount = models.FloatField()
    employee = models.ForeignKey(Worker, on_delete=models.CASCADE)
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    date = models.DateField()


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.worker.name} {self.worker.surname} ({self.get_leave_type_display()})"