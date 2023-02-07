from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import (
    ProfileEditForm,
    UserEditForm,
    UserRegistrationForm
)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'profile_form': profile_form, 'user_form': user_form})





