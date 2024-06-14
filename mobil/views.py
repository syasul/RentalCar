from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta

from django.db.models import Avg

from utils.currency import currency

from .models import Mobils
from testi.models import TestimonialRating

# Create your views here.
def masterMobil(request):
    current_user = request.user
    
    if not request.user.is_superuser:
        return redirect("user:loginAdmin")
        
        
    
    search_query = request.GET.get('search', '')
    mobils = Mobils.objects.all().order_by('-updated_at')

    if search_query:
        mobils = mobils.filter(name__icontains=search_query)

    for mobil in mobils:
        mobil.pricePerDay = currency(mobil.pricePerDay)

    context = {
        'mobils': mobils,
        'search_query': search_query,
    }
    return render(request, './admin/manageCar.html', context)


def createMobil(request):
    current_user = request.user
    
    if not request.user.is_superuser:
        return redirect("user:loginAdmin")
    
    if request.method == 'POST':
        nameOfCar = request.POST.get('nameOfCar')
        carImage1 = request.FILES['carImage1']
        carImage2 = request.FILES['carImage2']
        carImage3 = request.FILES['carImage3']
        stockCar = request.POST.get('stockCar')
        carDesc = request.POST.get('carDesc')
        transmission = request.POST.get('transmission')
        typecar= request.POST.get('typecar')
        seatOfCar = request.POST.get('seatOfCar')
        carPrice = request.POST.get('carPrice')
        
        Mobils.objects.create(
            name = nameOfCar,
            image1 = carImage1,
            image2 = carImage2,
            image3 = carImage3,
            pricePerDay = carPrice,
            transmission = transmission,
            typeCar = typecar,
            stock = stockCar,
            description = carDesc,
            seat = seatOfCar
            
        )
        
        return redirect("mobil:masterMobil")
    return redirect('mobil:masterMobil')

def updateMobil(request, id):
    current_user = request.user

    if not request.user.is_superuser:
        return redirect("user:loginAdmin")

    mobil = get_object_or_404(Mobils, pk=id)
    if request.method == 'POST':
        mobil.name = request.POST.get('nameOfCar')
        
        # Check if new image files are provided
        if 'carImage1' in request.FILES:
            mobil.image1 = request.FILES['carImage1']
        if 'carImage2' in request.FILES:
            mobil.image2 = request.FILES['carImage2']
        if 'carImage3' in request.FILES:
            mobil.image3 = request.FILES['carImage3']

        mobil.stock = request.POST.get('stockCar')
        mobil.description = request.POST.get('carDesc')
        mobil.transmission = request.POST.get('transmission')
        mobil.typeCar = request.POST.get('typecar')
        mobil.seat = request.POST.get('seatOfCar')
        mobil.pricePerDay = request.POST.get('carPrice')
        mobil.save()
        return redirect("mobil:masterMobil")

    return redirect('mobil:masterMobil')


def deleteMobil(request, id):
    current_user = request.user
    
    if not request.user.is_superuser:
        return redirect("user:loginAdmin")
    
    mobil = get_object_or_404(Mobils, pk=id)
    if request.method == 'POST':
        
        mobil.delete()
        
    
    return redirect('mobil:masterMobil')

def listCar(request):
    current_user = request.user
    
    # Get the filter parameters
    selected_categories = request.GET.getlist('category')
    selected_transmissions = request.GET.getlist('transmission')
    
    # Start with all cars
    mobils = Mobils.objects.all()
    
    # Filter by typeCar (category) if any selected
    if selected_categories:
        mobils = mobils.filter(typeCar__in=selected_categories)
    
    # Filter by transmission if any selected
    if selected_transmissions:
        mobils = mobils.filter(transmission__in=selected_transmissions)
    
    mobils_count = mobils.count()
    
    # Convert price per day to the desired format
    for mobil in mobils:
        mobil.pricePerDay = currency(mobil.pricePerDay)
    
    context = {
        'mobils': mobils, 
        'mobils_count': mobils_count,
        'current_user': current_user,
        'categories': ['Convertible', 'Coupe', 'Sedan', 'Hatchback', 'SUV', 'MPV'],  # Add more if necessary
        'selected_categories': selected_categories,
        'selected_transmissions': selected_transmissions
    }
    
    return render(request, 'user/listCar.html', context)

def detailCar(request, mobil_id):
    current_user = request.user
    
    testi_car = TestimonialRating.objects.filter(id_mobil=mobil_id)
    mobil = get_object_or_404(Mobils, id=mobil_id)
    
    mobil.pricePerDay = currency(mobil.pricePerDay)
    
    # Calculate the average rating
    average_rating = testi_car.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'user/detailCar.html', { 
        'mobils': mobil, 
        'current_user': current_user, 
        'ratings': testi_car, 
        'average_rating': round(average_rating, 1)
    })

