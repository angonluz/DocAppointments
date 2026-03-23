from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import calendar
from django.utils import timezone
from .models import Appointment
from .admin import AppointmentForm
from doctors.models import Doctor, Availability
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def get_available_slots(request):
    doctor_id = request.GET.get('doctor')
    date_str = request.GET.get('date')
    appt_id = request.GET.get('appointment_id')
    
    if not doctor_id or not date_str:
        return HttpResponse("<option value=''>Sub select Doctor and Date first</option>")
        
    try:
        query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        doctor = Doctor.objects.get(id=doctor_id)
    except (ValueError, Doctor.DoesNotExist):
        return HttpResponse("<option value=''>Invalid Date or Doctor</option>")
        
    day_of_week = query_date.weekday()
    availabilities = Availability.objects.filter(doctor=doctor, day_of_week=day_of_week)
    
    if not availabilities.exists():
        return HttpResponse("<option value=''>No availability on this day</option>")
        
    slots = []
    duration = timedelta(minutes=30)
    
    for avail in availabilities:
        current_time = datetime.combine(query_date, avail.start_time)
        end_dt = datetime.combine(query_date, avail.end_time)
        
        while current_time + duration <= end_dt:
            slots.append(current_time.time())
            current_time += duration
            
    existing_appointments = Appointment.objects.filter(doctor=doctor, date=query_date, status='scheduled')
    if appt_id:
        existing_appointments = existing_appointments.exclude(id=appt_id)
    
    available_slots = []
    for slot in slots:
        slot_end = (datetime.combine(query_date, slot) + duration).time()
        overlap = False
        for appt in existing_appointments:
            # Check overlap manually
            if max(slot, appt.start_time) < min(slot_end, appt.end_time):
                overlap = True
                break
        if not overlap:
            available_slots.append((slot, slot_end))
            
    if not available_slots:
        return HttpResponse("<option value=''>All booked for this day</option>")
        
    html = "<option value=''>Select a slot (30 mins)</option>"
    for start, end in available_slots:
        value = f"{start.strftime('%H:%M:%S')},{end.strftime('%H:%M:%S')}"
        label = f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"
        html += f"<option value='{value}'>{label}</option>"
        
    return HttpResponse(html)

@staff_member_required
def admin_calendar(request):
    year = int(request.GET.get('y', timezone.now().year))
    month = int(request.GET.get('m', timezone.now().month))
    
    cal = calendar.Calendar(firstweekday=6) # Sunday = 6
    month_days = cal.itermonthdates(year, month)
    
    start_date = date(year, month, 1) - timedelta(days=7)
    end_date = date(year, month, calendar.monthrange(year, month)[1]) + timedelta(days=7)
    
    appointments = Appointment.objects.filter(date__range=[start_date, end_date]).select_related('patient', 'doctor').order_by('start_time')
    
    appts_by_date = {}
    for appt in appointments:
        if appt.date not in appts_by_date:
            appts_by_date[appt.date] = []
        appts_by_date[appt.date].append(appt)
        
    weeks = []
    week = []
    for day in month_days:
        week.append({
            'date': day,
            'is_current_month': day.month == month,
            'is_today': day == timezone.now().date(),
            'appointments': appts_by_date.get(day, []),
            'is_past': day < timezone.now().date(),
        })
        if len(week) == 7:
            weeks.append(week)
            week = []
            
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
            
    context = {
        'weeks': weeks,
        'month_name': calendar.month_name[month],
        'year': year,
        'prev_m': prev_month,
        'prev_y': prev_year,
        'next_m': next_month,
        'next_y': next_year,
    }
    return render(request, 'admin/appointments/_calendar_grid.html', context)


@staff_member_required
def htmx_appointment_form(request):
    selected_date = request.GET.get('date')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return admin_calendar(request)
    else:
        initial = {}
        if selected_date:
            initial['date'] = selected_date
        form = AppointmentForm(initial=initial)
        
    return render(request, 'admin/appointments/_appointment_form_slideover.html', {'form': form, 'date': selected_date})

