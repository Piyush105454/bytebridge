from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Registration
from .forms import RegistrationForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Registration

def check_in(request, email):
    registration = get_object_or_404(Registration, email=email)
    registration.checked_in = True
    registration.save()
    return JsonResponse({"message": "Checked in successfully!"})

def check_out(request, email):
    registration = get_object_or_404(Registration, email=email)
    registration.checked_in = False
    registration.save()
    return JsonResponse({"message": "Checked out successfully!"})


def register(request):
    form = RegistrationForm()
    registration = None  # Initialize as None to avoid errors

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Registration.objects.filter(email=email).exists():
                return render(request, 'index.html', {'form': form, 'error': 'Email already registered!'})

            registration = form.save()  # Save the registration
            return redirect('index')  # Redirect to avoid resubmission

    return render(request, 'index.html', {'form': form, 'registration': registration})
