from .views import *
from django.urls import path

urlpatterns = [
    path('professor/register/', ProfessorRegisterView.as_view(), name='professor-register'),
    path('professor/login/', ProfessorLoginView.as_view(), name='professor-login'),  
    path('student/register/', StudentRegisterView.as_view(), name='student-register'),
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('professor/timeslot/create/', CreateTimeSlotView.as_view(), name='timeslot-create'),
    path('student/view_time_slots/', StudentViewTimeSlots.as_view(), name='student-view-time-slots'),
    path('student/book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path("professor/cancel_appointment/", CancelAppointmentView.as_view(), name="cancel_appointment"),
    path("student/check_appointments/", CheckAppointmentsView.as_view(), name="check_appointments"),
    
    
    
]

    
