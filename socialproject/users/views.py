from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegisterationForm
from .models import Profile
from .forms import UserEditForm,ProfileEditForm

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'], password=data["password"])
            if user is not None:
                login(request, user)
                return HttpResponse("User authenticated and logged in")
            else:
                return HttpResponse('Invalid Response')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def index(request):
    return render(request, 'users/index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit= False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user = new_user)
            return render(request, 'users/register_done.html')
    else:
        user_form = UserRegisterationForm()
    return render(request,'users/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance= request.user, data=request.POST)
        profile_form = ProfileEditForm(instance= request.user.profile, data=request.POST, files= request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance= request.user)
        profile_form = ProfileEditForm(instance= request.user.profile)
    return render(request,'users/edit.html',{'user_form':user_form,'profile_form':profile_form})