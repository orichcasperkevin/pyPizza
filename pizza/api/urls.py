from django.urls import path
from pizza.api import views

urlpatterns = [
    path('welcome/',views.Welcome.as_view()),
    path('topping/',views.Toppings.as_view(),name="topping"),
    path('finalize-order/<int:order_id>/',views.FinalizeOrder.as_view(),name="finalize")
]
