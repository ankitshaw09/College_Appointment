import re 
from .models import *
from datetime import time,datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class ProfessorRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    name = serializers.CharField(write_only=True)  # CustomUser's 'name' field
    college_id = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    user_type = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'college_id', 'department', 'email', 'user_type', 'password1', 'password2']

    def validate(self, data):
        # Check if email already exists
        if CustomUser.objects.filter(email=data['email']).exists():
            raise ValidationError("A user with this email already exists.")
        
        # Check if passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Validate password strength
        password = data['password1']
        self.validate_password_strength(password)
        return data
        
    def validate_password_strength(self, password):
        # Check for a minimum length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        # Check for at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")
        
        # Check for at least one number
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        
        # Check for at least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        # Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

    def create(self, validated_data):
        # Create the CustomUser instance first
        user = CustomUser.objects.create(
            name=validated_data['name'],
            college_id=validated_data['college_id'],
            department=validated_data['department'],
            email=validated_data['email'],
            user_type='professor'
        )
        user.set_password(validated_data['password1'])
        user.save()
        # Now create the Professor instance and link it to the CustomUser
        professor = Professor.objects.create(
            custom_user=user,
            name=validated_data['name'],
            college_id=validated_data['college_id'],
            department=validated_data['department'],
            email=validated_data['email'], # Same email as the CustomUser
            user_type='professor'  # Explicitly set user type as 'professor'
            )
        return professor

class ProfessorLoginSerializer(serializers.Serializer):
    college_id = serializers.CharField(max_length=10)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        college_id = data.get('college_id')
        password = data.get('password')
        
        user = authenticate(username=college_id, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid college ID or password.")
        
        # only professor  users can login
        if user.user_type!= 'professor':
            raise serializers.ValidationError("You are not authorized as a professor.")
        
        # Check if professor is active
        if not user.is_active:
            raise serializers.ValidationError("Account is not active.")
        
        data['user'] = user
        return data
        
class StudentRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    name = serializers.CharField(write_only=True)
    college_id = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    user_type = serializers.CharField(write_only=True)
    
    class Meta:
        model = Student
        fields = ['name', 'college_id', 'department', 'email','user_type', 'password1', 'password2']

    def validate(self, data):
        if CustomUser.objects.filter(email=data['email']).exists():
            raise ValidationError("A user with this email already exists.")
        
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
#     
        if data['user_type'] != 'student':
            raise serializers.ValidationError("Only student can register.")
        
        password=data['password1']
        self.validate_password_strength(password)
        return data
        
    def validate_password_strength(self, password):
        # Check if password has at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

    def create(self, validated_data):
        user = CustomUser.objects.create(
            name = validated_data['name'],
            college_id = validated_data['college_id'],
            department = validated_data['department'],
            email = validated_data['email'],
            user_type = 'student'
            )
        user.set_password(validated_data['password1'])
        user.save()
        student = Student.objects.create(
            custom_user=user,
            name = validated_data['name'],
            college_id = validated_data['college_id'],
            department = validated_data['department'],
            email = validated_data['email'],
            user_type = 'student'
            )
        return student
    
class StudentLoginSerializer(serializers.Serializer):
    college_id = serializers.CharField(max_length=10)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        college_id = data.get('college_id')
        password = data.get('password')
        
        user = authenticate(username=college_id, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid college ID or password.")
        
        # only student users can login
        if user.user_type!= 'student':
            raise serializers.ValidationError("You are not authorized as a student.")
        
        # Check if student is active
        if not user.is_active:
            raise serializers.ValidationError("Account is not active.")
        
        data['user'] = user
        return data

class TimeSlotSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format='%H:%M:%S')
    end_time = serializers.TimeField(format='%H:%M:%S')
    date = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model = TimeSlot
        fields = ['time_slot_id', 'date', 'start_time', 'end_time']

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        if start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")
        professor = self.context['request'].user
        existing_slots = TimeSlot.objects.filter(
            professor=professor,
            date=data['date']
        ).exclude(
            start_time__gte=end_time
        ).exclude(
            end_time__lte=start_time
        )
        if existing_slots.exists():
            raise serializers.ValidationError("Time slot overlaps with an existing slot.")  
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        professor = request.user  # Get the logged-in professor

        return TimeSlot.objects.create(
            time_slot_id=validated_data['time_slot_id'],
            professor=professor,
            professor_name=professor.name,
            professor_department=professor.department,
            date=validated_data['date'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time']
        )

class TimeSlotViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class BookAppointmentSerializer(serializers.Serializer):
    time_slot_id = serializers.CharField()
    student_name = serializers.CharField()
    student_college_id = serializers.CharField()
    student_department = serializers.CharField()

    def validate_time_slot_id(self, value):
        # Validate that the time slot exists
        try:
            time_slot = TimeSlot.objects.get(time_slot_id=value)
        except TimeSlot.DoesNotExist:
            raise serializers.ValidationError("Invalid time slot ID.")
        
        # Validate that the time slot is not already booked
        if hasattr(time_slot, 'appointment'):
            raise serializers.ValidationError("This time slot is already booked.")
        
        return time_slot

    def validate(self, data):
        # Ensure that the requesting user is authenticated and has the role of 'student'
        request = self.context.get('request')
        if not request.user.is_authenticated or request.user.user_type != 'student':
            raise serializers.ValidationError("Only authenticated students can book appointments.")
        return data

    def create(self, validated_data):
        # Get the logged-in student from the request context
        request = self.context.get('request')
        student = request.user
        
        # Extract time slot
        time_slot = validated_data['time_slot_id']

        # Create the Appointment record
        appointment = Appointment.objects.create(
            appointment_id=f"APT-{time_slot.time_slot_id}",
            student=student,
            student_name=validated_data['student_name'],
            student_college_id=validated_data['student_college_id'],
            student_department=validated_data['student_department'],
            professor=time_slot.professor,
            professor_name=time_slot.professor_name,
            professor_department=time_slot.professor_department,
            time_slot=time_slot,
            date=time_slot.date,
            start_time=time_slot.start_time,
            end_time=time_slot.end_time,
        )

        # Mark the time slot as booked
        time_slot.is_booked = True
        time_slot.save()

        return appointment

class CancelAppointmentSerializer(serializers.Serializer):
    appointment_id = serializers.CharField()

    def validate_appointment_id(self, value):
        try:
            appointment = Appointment.objects.get(appointment_id=value)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError("Invalid appointment ID. Appointment not found.")
        if appointment.is_cancelled:  # Correct field for checking cancellation
            raise serializers.ValidationError("This appointment is already cancelled.")
        return value

class CheckAppointmentsSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()

    def validate_student_id(self, value):
        if not Student.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid student ID.")
        return value

# 317