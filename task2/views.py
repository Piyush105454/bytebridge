from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from .models import Registration
from .forms import RegistrationForm
import threading

# Function to send reminder email
def send_reminder_email(email):
    send_mail(
        'Event Reminder',
        'Reminder: Your event is starting in 30 minutes!',
        'your_email@example.com',
        [email],
        fail_silently=False,
    )

# Registration View
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()

            # Send confirmation email
            send_mail(
                'Registration Successful',
                f'Thank you {registration.name}, you have successfully registered for the event!',
                'your_email@example.com',
                [registration.email],
                fail_silently=False,
            )

            # Schedule Reminder Email
            reminder_time = now() + timedelta(minutes=30)
            threading.Timer((reminder_time - now()).total_seconds(), send_reminder_email, [registration.email]).start()

            return JsonResponse({'message': 'Registration Successful!'})
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)

    return render(request, 'index.html', {'form': RegistrationForm()})
