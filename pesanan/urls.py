from django.urls import path

from . import views

urlpatterns = [
    path('form-checkout/<int:mobil_id>', views.formCheckout, name="formCheckout"),
    path('set-rental-dates/<int:mobil_id>', views.setRentalDates, name='setRentalDates'),
    path('my-order/', views.MyOrder, name="MyOrder"),
    path('return-order/<int:id_order>', views.returnOrder, name="returnOrder"),
    
    path('manage-order/', views.manageOrder, name="manageOrder"),
    path('update_status/<int:id_order>', views.updateStatus, name="updateStatus"),
    path('feedback-order/', views.feedbackOrder, name="feedbackOrder"),
    path('updateStatusFeedbackOrder/<int:id_order>', views.updateStatusFeedbackOrder, name="updateStatusFeedbackOrder")
]
