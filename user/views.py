from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .models import User

# Create your views here.
def loginAdmin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login_user(request, user)
                print('masuk admin')
                return redirect('dashboard')
            else:
                messages.error(request, 'You do not have admin privileges.')
                print("Kamu bukan admin")
        else:
            print("error user")
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin/loginAdmin.html')

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Retrieve the user by email
            user = User.objects.get(email=email)
            # Authenticate using the username and password
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                if authenticated_user.role == "User":
                    login_user(request, authenticated_user)
                    messages.success(request, 'Success login')
                    return redirect('home')
                else:
                    print('Invalid credentials')
            else:
                print('Invalid email or password')
        except User.DoesNotExist:
            print('Invalid email or password')
        except Exception as e:
            print('Error occurred: {e}')
        
    return render(request, 'user/loginUser.html')

def registerUser(request):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        hash_password = make_password(password)
        
        try:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return render(request, 'user/registerUser.html')

            user = User.objects.create(
                username=firstName +" "+lastName,
                email=email,
                password=hash_password,
                text_password=password,
                role="User"
            )
            
            # Authenticate and login the user
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                login_user(request, authenticated_user)
                messages.success(request, 'Registration successful and you are now logged in')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try again.')
        except Exception as e:
            messages.error(request, f'Error occurred: {e}')
        
    return render(request, 'user/registerUser.html')

def logout(request):
    current_user = request.user.role if request.user.is_authenticated else None
    logout_user(request)
    if current_user is not None and current_user == "User":
        return redirect('home')
    else:
        return redirect('user:loginAdmin')
