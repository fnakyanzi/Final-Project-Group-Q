from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.profile, name='profile'),
    
    #urls for the therapists
    path('therapist/dashboard/', views.therapist_dashboard, name='therapist_dashboard'),
    path('therapist/profile/edit/', views.edit_therapist_profile, name='edit_therapist_profile'),
    path('therapist/', views.therapist_directory, name='therapist_directory'),
    path('therapist/<int:pk>/', views.therapist_detail, name='therapist_detail'),
    path('therapist/appointments/', views.therapist_appointments, name='therapist_appointments'),
    path('appointment/<int:appointment_id>/mark/<str:status>/', views.mark_appointment_status, name='mark_appointment_status'),
    path('therapist/mode/', views.mode_settings, name='mode_settings'),

    
]