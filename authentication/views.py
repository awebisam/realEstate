from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
          # Check username
            if len(password) > 8:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'That username is taken')
                    return redirect('authentication:register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'That email is being used')
                        return redirect('authentication:register')
                    else:
                        # Looks good
                        user = User.objects.create_user(
                            username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                        '''Commented block to login right after register'''
                        # auth.login(request, user)
                        # messages.success(request, 'You are now logged in')
                        # return redirect('index')
                        user.save()
                        messages.success(
                            request, 'You are now registered and can log in')
                        return redirect('authentication:login')
            else:
                messages.error(request, 'Password is not strong enough')
                return redirect('authentication:register')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('authentication:register')
    else:
        return render(request, 'auth/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if User exists
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # Login user if user exists
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            if "next" in request.GET:
                return redirect('core_app:post')
            else:
                return redirect('core_app:index')
        else:
            # Give error if user doesn't exist
            messages.error(request, 'Invalid credentials')
            return redirect('authentication:login')
    else:
        return render(request, 'auth/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('core_app:index')
