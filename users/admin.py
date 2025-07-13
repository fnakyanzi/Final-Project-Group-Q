from django.contrib import admin
from .models import TherapistProfile, Appointment

@admin.register(TherapistProfile)
class TherapistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'speciality', 'availability', 'location', 'created_at')
    search_fields = ('user__username', 'speciality', 'location')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'therapist', 'date', 'status', 'created_at')
    search_fields = ('client__username', 'therapist__username', 'status')
    list_filter = ('status', 'date')
