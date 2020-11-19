import os

from django.conf import settings

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
#from .forms.CustomUserCreationForm import CustomUserCreationForm # con carpeta

from django.contrib.auth import login as make_login
from django.core.exceptions import ObjectDoesNotExist

from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile

# Create your views here.

def user_data(request):
    print(request.user.username)
    print(request.user.is_authenticated)
    return render(request,'user_data.html')

@login_required
def profile(request):
    #print(request.user.id)
    form = UserProfileForm()
    if request.method == 'POST':
        pathOldAvatar = None
        
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

            #path del avata anterior
            pathOldAvatar = os.path.join(settings.MEDIA_ROOT,userprofile.avatar.name)

        except ObjectDoesNotExist:
            form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():

            #borrar avatar anterior si existe un perfil
            if pathOldAvatar is not None and os.path.isfile(pathOldAvatar):
                os.remove(pathOldAvatar)

            userprofile = form.save(commit=False)
            userprofile.user = request.user
            userprofile.save()


    return render(request,'profile.html',{'form':form})

def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                make_login(request, user)
                return redirect(reverse('account:profile'))

            #return redirect(reverse('login'))

    return render(request,'register.html',{'form':form})