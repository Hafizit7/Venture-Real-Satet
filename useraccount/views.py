from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def register(request):
    if request.user.is_superuser == True:
        form = UserRegistrationForm()
        if request.method == "POST":
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.instance.is_staff = True
                form.save()
                messages.success(request, "Registration successful." )
                return redirect("register")
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request,'dashboard/user/register.html',{'form':form})
    else:
        return redirect('/')

@login_required
def register_view(request):
    query = User.objects.filter()
    return render(request,'dashboard/user/register_view.html',{'query':query})
    
@login_required
def register_edit(request,id):
    if request.user.is_superuser == True:
        query = User.objects.get(id=id)
        form = UserUpdateForm(instance = query)
        print(form)
        if request.method == "POST":
            form = UserUpdateForm(request.POST,instance = query)
            if form.is_valid():
                # form.instance.is_staff = True
                form.save()
                messages.success(request, "Update successful." )
                return redirect("register_view")
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request,'dashboard/user/register-update.html',{'form':form})
    else:
        return redirect('/')

def register_delete(request,id):
    query = User.objects.get(id=id)
    query.delete()
    return redirect('register_view')

def change_password(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    print(form)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user,data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
    return render(request, 'dashboard/user/change_password.html', {
        'form': form
    })
