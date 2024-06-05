from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta

from .models import Mobils

# Create your views here.
def masterMobil(request):
    mobils = Mobils.objects.all().order_by('-updated_at')
    
    context = {
        'mobils': mobils
    }
    return render(request, './admin/manageCar.html', context)

def createMobil(request):
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
    mobil = get_object_or_404(Mobils, pk=id)
    if request.method == 'POST':
        mobil.name = request.POST.get('nameOfCar')
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
    mobil = get_object_or_404(Mobils, pk=id)
    if request.method == 'POST':
        
        mobil.delete()
        
    
    return redirect('mobil:masterMobil')

def listCar(request):
    mobils = Mobils.objects.all()
    
    context = {
        'mobils': mobils
    }
    
    return render(request, 'user/listCar.html', context)

def detailCar(request, mobil_id):
    mobils = Mobils.objects.get(id=mobil_id)
    
    return render(request, 'user/detailCar.html', { 'mobils': mobils })

