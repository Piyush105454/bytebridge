from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Registration
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    request.session.flush()   # Logs out the user
    return redirect('register')  # Redirects to the home page (register page)

def register(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])  # Hash password
            
            if Registration.objects.filter(email=email).exists():
                return render(request, 'index.html', {'form': form, 'error': 'Email already registered!'})

            registration = form.save(commit=False)
            registration.password = password
            registration.save()

            # Send confirmation email
            try:
                send_mail(
                    'Registration Successful',
                    'You have successfully registered for the event.',
                    'your_email@example.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")

            return redirect('login')  # Redirect to login page after registration

    return render(request, 'index.html', {'form': form})
def login_view(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = Registration.objects.filter(email=email).first()
            if user and check_password(password, user.password):
                request.session['user_email'] = email  # Store session for authentication
                return redirect('register')  # Redirect to home page after login

            return render(request, 'index.html', {'form': form, 'error': 'Invalid credentials!'})

    return render(request, 'index.html', {'form': form})


@csrf_exempt
def check_in(request, email):
    if request.method == "POST":
        try:
            user = Registration.objects.get(email=email)
            if not user.checked_in:
                user.checked_in = True
                user.save()
                return render(request, 'index.html', {'message': "Check-in successful!", 'user': user})
            else:
                return render(request, 'index.html', {'message': "Already checked in!", 'user': user})
        except Registration.DoesNotExist:
            return render(request, 'index.html', {'message': "User not found!"})

    return redirect('register')  # Redirect if accessed via GET

@csrf_exempt
def check_out(request, email):
    if request.method == "POST":
        try:
            user = Registration.objects.get(email=email)
            if user.checked_in:
                user.checked_in = False
                user.save()
                return render(request, 'index.html', {'message': "Check-out successful!", 'user': user})
            else:
                return render(request, 'index.html', {'message': "Already checked out!", 'user': user})
        except Registration.DoesNotExist:
            return render(request, 'index.html', {'message': "User not found!"})

    return redirect('register')  # Redirect if accessed via GET
