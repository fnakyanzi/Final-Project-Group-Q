from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
import logging

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