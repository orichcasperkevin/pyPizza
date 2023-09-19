from django.urls import path
from pizza.api import views

urlpatterns = [
    path('answer-call/',views.AnswerCall.as_view()),
]
