from django.shortcuts import render, redirect
from django.contrib.auth import login , logout , authenticate, get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated



# Create your views here.
@user_not_authenticated
def register(request):
    if request.method== "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Succesful registration! {user.username}")
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                
    else:
        form = UserRegistrationForm()
        
    return render(
        request=request,
        template_name= "users/register.html",
        context={"form":form}
    )


@login_required
def custom_logout (request):
    logout(request)
    messages.info(request, "You have logged out from your account!")
    return redirect("homepage")
@user_not_authenticated
def custom_login(request):
    if request.method== "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate (
                username=form.cleaned_data["username"], 
                password=form.cleaned_data["password"],
            )
            #if the user is authenticated and exists
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username} </b> Succesful login!")
                return redirect("homepage")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            
    form = UserLoginForm()
    return render(
        request=request,
        template_name= "users/login.html",
        context={"form":form}
    )

def profile(request, username):
    if request.method== 'POST':
        user= request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form=form.save()
            messages.success(request, f'{user_form.username}, Your profile has been changed!')
            return redirect("profile", user_form.username)
        
        for error in list(form.errors.values()):
                messages.error(request, error)
        
    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name= "users/profile.html",
            context={"form":form}
    )
    return redirect("homepage")