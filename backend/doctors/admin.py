from django.contrib import admin
from .models import Specialty, Doctor, Availability

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'email', 'phone')
    list_filter = ('specialty',)
    search_fields = ('name', 'email')
    inlines = [AvailabilityInline]

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('doctor', 'day_of_week')
