from django.db import models
from django.utils import timezone
from user.models import User
from mobil.models import Mobils

class Order(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    grand_total = models.BigIntegerField()
    STATUS_CHOICES = (
        ("Belum Terkonfirmasi", "Belum Terkonfirmasi"),
        ("Terkonfirmasi", "Terkonfirmasi"),
        ("Dikirim", "Dikirim"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_receipt_image_path = models.ImageField(upload_to="images/")
    photo_kk = models.ImageField(upload_to="images/")
    photo_ktp = models.ImageField(upload_to="images/")
    telephone = models.IntegerField()
    address = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fine = models.BigIntegerField(default=0)

    def hitung_fine(self):
        if self.status == 'Dikirim' and self.end_date < timezone.now().date():
            hari_keterlambatan = (timezone.now().date() - self.end_date).days
            self.fine = (self.grand_total * 0.02) * hari_keterlambatan if hari_keterlambatan > 0 else 0
        else:
            self.fine = 0

    def save(self, *args, **kwargs):
        self.hitung_fine()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order with id : {self.id}"

class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_mobils = models.ForeignKey(Mobils, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class ReturnOrder(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    photo_payment_fine = models.ImageField(upload_to='images/', null=True, blank=True)
    STATUS_CHOICES = [
        ('Dikembalikan', 'Dikembalikan'),
        ('Diterima', 'Diterima'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Dikembalikan')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.id_order.fine > 0:
            if not self.photo_payment_fine:
                raise ValueError("Foto pembayaran denda wajib diunggah untuk pengembalian terlambat")
        super().save(*args, **kwargs)