from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
