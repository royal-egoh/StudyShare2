from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from .models import CustomUser, FACULTY_DEPARTMENT_MAP, FACULTY_CHOICES, DEPARTMENT_CHOICES

def login_view(request):
    # login(request, request.user, backend='allauth.account.auth_backends.AuthenticationBackend')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def register(request):
    email = request.user.email
    current_user = CustomUser.objects.get(email=email)

    if current_user.department and current_user.level:
        return redirect('home')
    
    if request.method == 'POST':
        faculty = request.POST.get('faculty')
        department = request.POST.get('department')
        level = request.POST.get('level')
        current_user.faculty = faculty
        current_user.department = department
        current_user.level = level
        current_user.save()
        messages.success(request, f'Logged in as {current_user.username}')
        return redirect('home')
    return render(request, 'register.html', {'fac_choices': FACULTY_CHOICES, 'dep_choices': DEPARTMENT_CHOICES})

