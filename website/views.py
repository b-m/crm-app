from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None: 
            login(request, user)
            messages.success(request, f'User {username} logged in!')            
        else:
            messages.error(request, f'Error loggin in {username}!')

        #return redirect('home')
    #else: 
    return render(request, 'home.html', {'records': records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
def show_record(request, pk):
    if request.user.is_authenticated:
        cus_rec = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': cus_rec})
    else:
        messages.error(request, 'You must be logged in to view customer records.')
        return redirect('home')

def delete_record(request, pk):
    delete_it = Record.objects.get(id=pk)
    if delete_it:
        delete_it.delete()
        messages.success(request, '1 record deleted successfully.')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in to delete customer record.')
        return redirect('home')
