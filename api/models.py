from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    number_of_employees = models.IntegerField()

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    salary = models.FloatField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Administrator(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Day(models.Model):
    worked = models.BooleanField()
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
    TYPE_CHOICES = [
        ('sick', 'Больничный'),
        ('vacation', 'Отпуск'),
    ]

    full_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.full_name} ({self.get_leave_type_display()})"