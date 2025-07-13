from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
import logging

from .models import TherapistProfile
from django.shortcuts import get_object_or_404
from users.models import Appointment
from django.contrib.auth import get_user_model


from .forms import TherapistProfileForm
from django.contrib.auth.decorators import login_required

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def home(request):
    user_group = None
    if request.user.is_authenticated:
        logger.debug(f"User: {request.user.username}, Groups: {[g.name for g in request.user.groups.all()]}")
        if request.user.groups.exists():
            user_group = request.user.groups.first().name
            logger.debug(f"Assigned user_group: {user_group}")
        else:
            logger.debug("No groups found for user")
    return render(request, 'users/home.html', {'user_group': user_group})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            client_group = Group.objects.get(name='Client')
            user.groups.add(client_group)
            logger.debug(f"Assigned Client group to {user.username}")
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'You do not have permission to access this page.')
        return HttpResponseForbidden('Forbidden')
    return render(request, 'users/admin_dashboard.html', {'user': request.user})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_group = request.user.groups.first().name if request.user.groups.exists() else None
    return render(request, 'users/profile.html', {'user': request.user, 'user_group': user_group})

##therapist views by faridah
@login_required
def therapist_dashboard(request):
    profile = TherapistProfile.objects.filter(user=request.user).first()
    appointments = Appointment.objects.filter(therapist = request.user).order_by("date")
    return render(request, "therapist/therapist_dashboard.html",{
        "profile": profile,
        "appointments": appointments
    })
   
@login_required
def edit_therapist_profile(request):
    profile, created = TherapistProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = TherapistProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("therapist_dashboard")
    else:
        form = TherapistProfileForm(instance=profile)

    return render(request, "therapist/edit_profile.html", {"form": form})

#therapist directory for his clients
def therapist_directory(request):
    therapists = TherapistProfile.objects.all()
    query = request.GET.get("q")
    if query:
        therapists = therapists.filter(speciality__icontains=query)
    return render(request, "therapist/directory.html",{"therapists": therapists})
 
def therapist_detail(request, pk):
    therapist = get_object_or_404(TherapistProfile, pk=pk)
    return render(request, 'therapist/detail.html',{"therapist": therapist})

#appointments
@login_required
def therapist_appointments(request):
    appointments = Appointment.objects.filter(therapist=request.user).order_by('date')
    return render(request, "therapist/appointments.html", {"appointments": appointments})

#mark appointemnts
@login_required
def mark_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id, therapist=request.user)
    if status in ['confirmed', 'completed', 'cancelled']:
        appointment.status = status
        appointment.save()
    return redirect('therapist_dashboard')
#setting
@login_required
def mode_settings(request):
    return render(request, "therapist/mode.html")
