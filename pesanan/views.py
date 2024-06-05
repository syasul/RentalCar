from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ValidationError

from mobil.models import Mobils
from pesanan.models import Order, OrderItem, ReturnOrder
from testi.models import TestimonialRating

@login_required
def setRentalDates(request, mobil_id):
    if request.method == 'POST':
        check_in = request.POST.get('checkIn')
        check_out = request.POST.get('checkOut')
        start_date = datetime.strptime(check_in, '%Y-%m-%d')
        end_date = datetime.strptime(check_out, '%Y-%m-%d')

        if start_date >= end_date:
            messages.error(request, 'Check-out date must be after check-in date.')
            return redirect('pesanan:formCheckout', mobil_id=mobil_id)

        request.session['check_in'] = check_in
        request.session['check_out'] = check_out
        return redirect('pesanan:formCheckout', mobil_id=mobil_id)

    return redirect('pesanan:formCheckout', mobil_id=mobil_id)

@login_required
def formCheckout(request, mobil_id):
    mobils = get_object_or_404(Mobils, id=mobil_id)
    current_user = request.user
    check_in = request.session.get('check_in')
    check_out = request.session.get('check_out')

    if not check_in or not check_out:
        messages.error(request, 'Please select check-in and check-out dates first.')
        return redirect('mobil:detailCar', mobil_id=mobil_id)

    start_date = datetime.strptime(check_in, '%Y-%m-%d')
    end_date = datetime.strptime(check_out, '%Y-%m-%d')
    total_days = (end_date - start_date).days
    total_price = total_days * mobils.pricePerDay

    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        address = request.POST.get('address')
        photo_kk = request.FILES['uploadKK']
        photo_ktp = request.FILES['uploadKTP']
        payment_receipt_image_path = request.FILES['uploadPurchace']

        order = Order.objects.create(
            id_user=current_user,
            start_date=start_date,
            end_date=end_date,
            grand_total=total_price,
            status="Belum Terkonfirmasi",
            payment_receipt_image_path=payment_receipt_image_path,
            photo_kk=photo_kk,
            photo_ktp=photo_ktp,
            telephone=telephone,
            address=address
        )

        OrderItem.objects.create(
            id_order=order,
            id_mobils=mobils,
            quantity=1
        )

        mobils.stock -= 1
        mobils.save()

        request.session.pop('check_in', None)
        request.session.pop('check_out', None)

        messages.success(request, 'Order berhasil dibuat!')
        return redirect('pesanan:MyOrder')

    return render(request, 'user/formCheckout.html', {'mobils': mobils, 'user': current_user, 'totalPrice': total_price})

@login_required
def MyOrder(request):
    current_user = request.user
    orders = Order.objects.filter(id_user=current_user).order_by('-start_date')
    return render(request, 'user/pesananSaya.html', {'orders': orders})

def manageOrder(request):
    orders = Order.objects.all()
    return render(request, 'admin/manageOrder.html', {'orders': orders})

@login_required
def updateStatus(request, id_order):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order.objects.get(pk=id_order)
        order.status = status
        order.save()
    return redirect('pesanan:manageOrder')
    
@login_required
def returnOrder(request, id_order):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=id_order)
        orderItem = get_object_or_404(OrderItem, id_order=order)  # Perbaikan di sini
        
        # Get testimonial data
        rating = request.POST.get('rating')
        content_testimonial = request.POST.get('contentTestimonial')
        
        # Get return order image
        image = request.FILES.get('image')

        # Create and save TestimonialRating
        if rating and content_testimonial:
            testimonial = TestimonialRating(
                id_user=request.user,
                id_mobil=orderItem.id_mobils,
                contentTestimonial=content_testimonial,
                rating=int(rating)
            )
            testimonial.save()

        # Create and save ReturnOrder
        if image:
            return_order = ReturnOrder(
                id_order=order,
                image=image,
                status="Dikembalikan"
            )
            try:
                return_order.save()
            except ValidationError as e:
                # Handle validation error, e.g., missing photo_payment_fine
                print(e)
                return redirect('pesanan:MyOrder')

        return redirect('pesanan:MyOrder')
    else:
        return redirect('pesanan:MyOrder')

@login_required
def feedbackOrder(request):
    returnOrders = ReturnOrder.objects.all()
    ratings = TestimonialRating.objects.all()
    data = list(returnOrders) + list(ratings)
    return render(request, 'admin/feedbackOrder.html', {'ratings': ratings})

@login_required
def updateStatusFeedbackOrder(request,id_order):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = ReturnOrder.objects.get(pk=id_order)
        order.status = status
        order.save()
    return redirect('pesanan:manageOrder')
    
    