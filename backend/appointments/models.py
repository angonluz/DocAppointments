from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from doctors.models import Doctor, Availability
from patients.models import Patient

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date} at {self.start_time}"

    def clean(self):
        if not self.start_time or not self.end_time or not self.date or not self.doctor:
            return

        if self.date < timezone.now().date():
            raise ValidationError({'date': "Cannot schedule appointments in the past."})

        if self.start_time >= self.end_time:
            raise ValidationError({'start_time': "Start time must be before end time."})

        # Check doctor availability
        day_of_week = self.date.weekday()
        availabilities = Availability.objects.filter(
            doctor=self.doctor,
            day_of_week=day_of_week,
            start_time__lte=self.start_time,
            end_time__gte=self.end_time
        )
        
        if not availabilities.exists():
            raise ValidationError(f"Doctor {self.doctor.name} is not available at this time on {self.date.strftime('%A')}.")

        # Check for overlaps
        overlapping_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            date=self.date,
            status='scheduled'
        ).exclude(pk=self.pk).filter(
            models.Q(start_time__lt=self.end_time, end_time__gt=self.start_time)
        )

        if overlapping_appointments.exists():
            raise ValidationError(f"Doctor {self.doctor.name} already has an appointment during this time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
