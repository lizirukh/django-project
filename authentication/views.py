from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


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

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid:
            form.save(
                request=request,
                use_https=False,
                email_template_name='registration/password_reset_email.html',
            )

            return HttpResponse('<h2> Reset email has been successfully sent, Please check your email to finish the process. </h2')

    else:
        form = PasswordResetForm()
        return render(request, 'registration/password_reset_request.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    try:
        id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=id)

        if default_token_generator.check_token(user, token):
            if request.method =='POST':
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()

                    return redirect('login')
            else:
                form = SetPasswordForm(user=user)
        else:
            return HttpResponse('<h2> Password reset token is invalid </h2>')

    except (User.DoesNotExist, ValueError):
        return redirect('password_reset')

    return render(request, 'password_reset_confirm.html', {'form': form})