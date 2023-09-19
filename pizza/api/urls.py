from django.urls import path
from pizza.api import views

urlpatterns = [
    path('answer-call/',views.AnswerCall.as_view()),
    path('welcome/',views.Welcome.as_view()),
    path('menu/',views.Menu.as_view(),name="menu")
]
