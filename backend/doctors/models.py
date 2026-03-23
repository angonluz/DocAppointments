from django.db import models

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name='doctors')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"

class Availability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Availabilities"
        unique_together = ('doctor', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_of_week_display()}: {self.start_time} to {self.end_time}"
