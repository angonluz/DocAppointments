from django import forms
from django.contrib import admin
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    slot_selection = forms.CharField(
        widget=forms.Select(choices=[('', '-------')]), 
        required=False, 
        help_text="Select a time slot (populates Start and End time automatically)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure start and end times are strictly required in the form
        self.fields['start_time'].required = True
        self.fields['end_time'].required = True
        
        # Add appointment_id if instance exists to exclude it from overlap checks
        url = '/appointments/get-slots/'
        if self.instance and self.instance.pk:
            url += f'?appointment_id={self.instance.pk}'
            
        self.fields['doctor'].widget.attrs['hx-get'] = url
        self.fields['date'].widget.attrs['hx-get'] = url

    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'doctor': forms.Select(attrs={
                'hx-target': '#id_slot_selection', 
                'hx-include': '[name="date"]',
                'hx-trigger': 'change, load'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'hx-trigger': 'change, keyup delay:500ms',
                'hx-target': '#id_slot_selection', 
                'hx-include': '[name="doctor"]'
            }),
        }

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ('patient', 'doctor', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__name', 'doctor__name')
    date_hierarchy = 'date'

    fieldsets = (
        ('Patient Info', {
            'fields': ('patient', 'doctor')
        }),
        ('Scheduling (Select Date & Doctor to load slots)', {
            'fields': ('date', 'slot_selection', 'start_time', 'end_time')
        }),
        ('Details', {
            'fields': ('status', 'notes')
        }),
    )

    class Media:
        js = (
            'https://unpkg.com/htmx.org@1.9.10', 
            'js/htmx_admin.js',
        )
