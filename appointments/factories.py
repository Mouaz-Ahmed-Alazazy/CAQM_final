from datetime import datetime, timedelta
from .models import Appointment, DoctorAvailability

class AppointmentFactory:
    """
    Factory for creating Appointment objects.
    Encapsulates complex logic for appointment creation.
    """
    
    @staticmethod
    def create_appointment(patient, doctor, appointment_date, start_time, notes=''):
        """
        Create and return an Appointment instance (unsaved).
        validates availability and calculates end time.
        """
        # Calculate end time based on slot duration
        day_of_week = appointment_date.strftime('%A').upper()
        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            day_of_week=day_of_week,
            is_active=True
        ).first()
        
        if not availability:
            raise ValueError('Doctor is not available on this day')
        
        start_datetime = datetime.combine(appointment_date, start_time)
        end_datetime = start_datetime + timedelta(minutes=availability.slot_duration)
        end_time = end_datetime.time()
        
        # Create appointment instance
        return Appointment(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            notes=notes,
            status='SCHEDULED'
        )
