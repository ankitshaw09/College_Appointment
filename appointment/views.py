from .models import *
from .serializers import *
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.authtoken.models import Token  # Use for Token Authentication


class ProfessorRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allows anyone to access this endpoint
    queryset = Professor.objects.all()  # Queryset is defined for creating objects
    serializer_class = ProfessorRegisterSerializer  # Use the defined serializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            professor = serializer.save()
            return Response({
                "message": "Registered successfully",
                "name": professor.name,
                "college_id": professor.college_id,
                "department": professor.department,
                "email": professor.email,
                "user_type": professor.user_type
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfessorLoginView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to access this endpoint
    def post(self, request, *args, **kwargs):
        serializer = ProfessorLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful.',
                'name': user.name,
                'college_id': user.college_id,
                'department': user.department,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    
class StudentRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allows anyone to access this endpoint
    queryset = Student.objects.all()  # Queryset is defined for creating objects
    serializer_class = StudentRegisterSerializer  # Use the defined serializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "message": "Registered successfully",
                "name": student.name,
                "college_id": student.college_id,
                "department": student.department,
                "email": student.email,
                "user_type": student.user_type
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentLoginView(APIView):
    permission_classes = [AllowAny]  # Allows anyone to access this endpoint
    def post(self, request, *args, **kwargs):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful.',
                'name': user.name,
                'college_id': user.college_id,
                'department': user.department,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CreateTimeSlotView(generics.CreateAPIView):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        if request.user.user_type != 'professor':
            return Response(
                {"message": "Only professors can create time slots."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            time_slot = serializer.save()
            return Response({
                "message": "Time slot created successfully",
                "time_slot_id": time_slot.time_slot_id,
                "name": time_slot.professor_name,
                "department": time_slot.professor_department,
                "date": time_slot.date,
                "start_time": time_slot.start_time,
                "end_time": time_slot.end_time
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentViewTimeSlots(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the student is authenticated
    def get(self, request, *args, **kwargs):
        student = request.user
        time_slots = TimeSlot.objects.all()
        
        if request.user.user_type != 'student':
            return Response({"detail": "Only students can view available time slots."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TimeSlotViewSerializer(time_slots, many=True)
        return Response({
            "message": "Available time slots retrieved successfully.",
            "time_slots": serializer.data
        }, status=status.HTTP_200_OK)
        
class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type != 'student':
            return Response(
                {"message": "Only students can book appointments."},
                status=status.HTTP_403_FORBIDDEN,
            )

        time_slot_id = request.data.get("time_slot_id")
        if not time_slot_id:
            return Response(
                {"message": "Time slot ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            time_slot = TimeSlot.objects.get(time_slot_id=time_slot_id)
        except TimeSlot.DoesNotExist:
            return Response(
                {"message": "Invalid time slot ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if Appointment.objects.filter(time_slot=time_slot).exists():
            return Response(
                {"message": "This time slot is already booked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment = Appointment.objects.create(
            appointment_id=f"A{time_slot_id}",  # Generate a unique appointment ID
            student=user,
            student_name=user.name,
            student_college_id=user.college_id,
            student_department=user.department,
            professor=time_slot.professor,
            professor_name=time_slot.professor_name,
            professor_department=time_slot.professor_department,
            time_slot=time_slot,  # Pass the actual `TimeSlot` instance, not its ID
            date=time_slot.date,
            start_time=time_slot.start_time,
            end_time=time_slot.end_time,
            is_cancelled=False,
        )
        
        # Mark the time slot as booked
        time_slot.is_booked = True
        time_slot.save()

        return Response(
            {
                "message": "Appointment booked successfully.",
                "appointment_id": appointment.appointment_id,
                "time_slot_id": appointment.time_slot_id,
                "student_name": appointment.student_name,
                "student_college_id": appointment.student_college_id,
                "student_department": appointment.student_department,
                "professor_name": appointment.professor_name,
                "professor_department": appointment.professor_department,
                "date": appointment.date,
                "start_time": appointment.start_time,
                "end_time": appointment.end_time,
            },
            status=status.HTTP_201_CREATED,
        )

class CancelAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CancelAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment_id = serializer.validated_data["appointment_id"]

            try:
                appointment = Appointment.objects.get(appointment_id=appointment_id)
                if( request.user != appointment.student and request.user != appointment.professor):
                    return Response(
                        {"message": "You do not have permission to cancel this appointment."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                    # Update time slot to available
                appointment.time_slot.is_booked = False
                appointment.time_slot.save()
                appointment.is_cancelled = True
                appointment.save()
                return Response(
                    {"message": f"Appointment {appointment_id} has been cancelled successfully."},
                    status=status.HTTP_200_OK,
                )
            except Appointment.DoesNotExist:
                return Response(
                    {"message": "Appointment not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request, *args, **kwargs):
        user = request.user
        try :
            student = Student.objects.get(custom_user=user)
        except Student.DoesNotExist:
            return Response(
                {"message": "Only students can check their appointments."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Fetch the student's pending appointments
        pending_appointments = Appointment.objects.filter(
            student=user, is_cancelled=False
        )
        if not pending_appointments.exists():
            return Response(
                {"message": "You do not have any pending appointments."},
                status=status.HTTP_200_OK,
            )
        appointments_data = [
            {
                "appointment_id": appointment.appointment_id,
                "professor_name": appointment.professor_name,
                "professor_department": appointment.professor_department,
                "date": appointment.date,
                "start_time": appointment.start_time,
                "end_time": appointment.end_time,
            }
            for appointment in pending_appointments
        ]
        return Response(
            {"message": "Here are your pending appointments.", "appointments": appointments_data},
            status=status.HTTP_200_OK,
        )
        
class CheckProfessorAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated  
    def get(self, request, *args, **kwargs):
        user = request.user
        try :
            professor = Professor.objects.get(custom_user=user)
        except Professor.DoesNotExist:
            return Response(
                {"message": "Only professors can check their appointments."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Fetch the professor's appointments
        appointments = Appointment.objects.filter(
            professor=user, is_cancelled=False
        )
        if not appointments.exists():
            return Response(
                {"message": "You do not have any appointments."},
                status=status.HTTP_200_OK,
            )
        
        appointments_data = [
            {
                "appointment_id": appointment.appointment_id,
                "student_name": appointment.student_name,
                "student_college_id": appointment.student_college_id,
                "student_department": appointment.student_department,
                "date": appointment.date,
                "start_time": appointment.start_time,
                "end_time": appointment.end_time,
            }
            for appointment in appointments
        ]
        return Response(
            {"message": "Here are your appointments.", "appointments": appointments_data},
            status=status.HTTP_200_OK,
        )
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            # Use blacklist() if blacklist feature is enabled
            try:
                token.blacklist()
            except AttributeError:
                return Response(
                    {"detail": "Token blacklist feature is not enabled."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 303

