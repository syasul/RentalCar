from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.contrib import messages

from pesanan.models import Order, ReturnOrder, OrderItem
from django.contrib.auth.decorators import login_required
from user.models import User
from mobil.models import Mobils
from testi.models import TestimonialRating

from utils.currency import currency

def home(request):
    mobils = Mobils.objects.all()
    ratings = TestimonialRating.objects.all()
    current_user = request.user
    
    for mobil in mobils:
        mobil.pricePerDay = currency(mobil.pricePerDay)
        
    
    return render(request, './user/home.html', {'current_user': current_user, 'mobils': mobils, 'ratings':ratings})

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect("user:loginAdmin")
    
    order_items = Order.objects.all().prefetch_related('orderitem_set__id_mobils').order_by('-updated_at')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            checkin = datetime.strptime(start_date, '%Y-%m-%d')
            checkout = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
            return redirect('dashboard')

        if checkin >= checkout:
            messages.error(request, 'Check-out date must be after check-in date.')
            return redirect('dashboard')
        
        order_items = order_items.filter(start_date__gte=start_date, end_date__lte=end_date)

    mobils_count = Mobils.objects.count()
    order_count = Order.objects.count()
    return_order_count = TestimonialRating.objects.count()
    user_count = User.objects.filter(is_superuser=False).count()
    
    grand_total_count = Order.objects.aggregate(total=Sum('grand_total'))['total'] or 0
    grand_fine_count = Order.objects.aggregate(total=Sum('fine'))['total'] or 0
    
    income_count = grand_total_count + grand_fine_count
    income_counts = currency(income_count)
    
    for order in order_items:
        order.grand_total = currency(order.grand_total)

    context = {
        'order_items': order_items,
        'mobils_count': mobils_count,
        'order_count': order_count,
        'user_count': user_count,
        'return_order_count': return_order_count,
        'income_count': income_counts,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
def generate_pdf(request):
    template_path = 'admin/dashboard_pdf.html'
    orders = Order.objects.all().order_by('-updated_at')
    
    start_date = request.GET.get('start_date')  # Mendapatkan start_date dari requestat
    end_date = request.GET.get('end_date')      # Mendapatkan end_date dari request
    
    if start_date and end_date:
        orders = orders.filter(start_date__gte=start_date, end_date__lte=end_date)  # Menyaring data berdasarkan tanggal
    
    context = {'orders': orders}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="export_keuangan.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response

def Contact(request):
    current_user = request.user
    return render(request, 'user/contact.html', {'current_user': current_user})
    
    