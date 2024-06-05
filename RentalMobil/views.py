from django.shortcuts import render

def home(request):
    return render(request, './user/home.html')

def dashboard(request):
    return render(request, './admin/dashboard.html')
    