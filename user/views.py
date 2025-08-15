from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from user.forms import CustomRegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator







def sign_up(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, 'A confirmation email has been sent. Please check your inbox.')
            return redirect('sign-in')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. You can now log in.')
            return redirect('sign-in')
        else:
            messages.error(request, 'Invalid activation link.')
            return redirect('sign-up')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('sign-up')
    

