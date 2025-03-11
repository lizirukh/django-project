from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('books_list')
        else:
            return render(request, 'registration/registration.html', {'form': form})

    else:
        form = RegistrationForm()

        return render(request, 'registration/registration.html', {'form': form})


def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('books_list')

        else:
            return redirect(request, 'registration/login.html', {'form': form})

    else:
        form = AuthenticationForm()

        return render(request, 'registration/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('books_list')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            update_session_auth_hash(request, request.user)

            return redirect('books_list')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'registration/change_password.html', {'form': form})