from django.urls import path
from . import views

urlpatterns = [
    path('get-slots/', views.get_available_slots, name='get-slots'),
    path('admin-calendar/', views.admin_calendar, name='admin-calendar'),
    path('admin-calendar-form/', views.htmx_appointment_form, name='htmx-appointment-form'),
]
