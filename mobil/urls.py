from django.urls import path

from . import views

urlpatterns = [
    path('list-car/', views.listCar, name="listCar"),
    path('detail-car/<int:mobil_id>', views.detailCar, name="detailCar"),
    
    path('master-mobil/', views.masterMobil, name="masterMobil"),
    path('create-mobil/', views.createMobil, name="createMobil"),
    path('update-mobil/<int:id>', views.updateMobil, name="updateMobil"),
    path('delete-mobil/<int:id>', views.deleteMobil, name="deleteMobil")
]