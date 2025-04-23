from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CitizenSignupForm, AdminSignupForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import UserLoginAttempt  # Import the model for saving login attempts (defined below)

User = get_user_model()


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        return HttpResponse("✅ Email verified successfully! You can now log in.")
    else:
        return HttpResponse("❌ Verification link is invalid or expired.")


def Signup(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'citizen':
            form = CitizenSignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('login')  # Redirect to login page after successful signup
        elif role == 'admin':
            form = AdminSignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('login')  # Redirect to login page after successful signup
    else:
        # Display the Citizen form initially (or both if you want to allow a choice)
        form = CitizenSignupForm()

    return render(request, 'Signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Log the login attempt
                UserLoginAttempt.objects.create(user=user, successful=True)
                
                messages.success(request, "Login successful!")
                return redirect('homepage')  # Redirect to the homepage

            else:
                # If authentication failed, log the failed attempt
                user = User.objects.filter(username=username).first()
                if user:
                    UserLoginAttempt.objects.create(user=user, successful=False)

                messages.error(request, "Invalid username or password!")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def Homepage(request):
    return render(request, 'index.html')

def Report(request):
    return render(request, 'Report.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    request.session.flush()  # Optional: extra cleanup
    return redirect('homepage')
