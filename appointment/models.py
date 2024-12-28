from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, college_id, name, department, email, password=None, user_type=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            college_id=college_id,
            name=name,
            department=department,
            email=email,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, college_id, name, department, email, password=None, user_type=None):
        user = self.create_user(
            college_id=college_id,
            name=name,
            department=department,
            email=email,
            password=password,
            user_type=user_type
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = (
        ('professor', 'Professor'),
        ('student', 'Student'),
    )
    name = models.CharField(max_length=100)
    college_id = models.CharField(unique=True, max_length=10)
    department = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES)
    password = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'email', 'department']
    USERNAME_FIELD = 'college_id'

    objects = CustomUserManager()
    def __str__(self):
        return self.name

class Professor(models.Model):
    custom_user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    college_id = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=CustomUser.ROLE_CHOICES, default='professor')
    def __str__(self):
        return self.custom_user.name

class Student(models.Model):
    custom_user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    college_id = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=CustomUser.ROLE_CHOICES, default='student')
    def __str__(self):
        return self.custom_user.name

class TimeSlot(models.Model):
    time_slot_id = models.CharField(max_length=10, unique=True)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    professor_name = models.CharField(max_length=100)
    professor_department = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.professor.name} ({self.professor.department}) - {self.date} {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    appointment_id = models.CharField(max_length=10, unique=True)
    # Student Details
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_appointments"  # Distinct related name for student
    )
    student_name = models.CharField(max_length=100)
    student_college_id = models.CharField(max_length=10)
    student_department = models.CharField(max_length=100)
    # Professor Details
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professor_appointments"  # Distinct related name for professor
    )
    professor_name = models.CharField(max_length=100)
    professor_department = models.CharField(max_length=100)
    # Time Slot
    time_slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name="appointment"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Status
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.professor_name} & {self.student_name}"

# 129