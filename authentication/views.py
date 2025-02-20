from django.shortcuts import render, redirect
from .forms import RegistrationForm


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
