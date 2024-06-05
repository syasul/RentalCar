from django.db import models

from mobil.models import Mobils
from user.models import User
from pesanan.models import ReturnOrder

# Create your models here.
class TestimonialRating(models.Model):
    id_mobil = models.ForeignKey(Mobils, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_return_order = models.ForeignKey(ReturnOrder, on_delete=models.CASCADE, default=1)
    contentTestimonial = models.CharField(max_length=200)
    rating = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
