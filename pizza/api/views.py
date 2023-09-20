from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from twilio.twiml.voice_response import VoiceResponse
from pizza.models import OrderMessageConfig,Crust,Order,Topping

class AnswerCall(APIView):
    def post(self, request):
        """Respond to incoming phone calls with a brief message."""
        # Start our TwiML response
        resp = VoiceResponse()

        # Read a message aloud to the caller
        resp.say("Thank you for calling! Have a great day.", voice='Polly.Amy')

        return Response(str(resp),status =status.HTTP_200_OK,content_type='text/xml')


class Welcome(APIView):
    def post(self,request):
        """
            Respond to incoming calls, give the users options
        """
        #construct the message
        message = OrderMessageConfig.objects.first().welcome_message
        #add the crust options
        for i,crust in enumerate( Crust.objects.all() ):
            message +=  f" press {crust.size} for {crust.display_name},"
        response = VoiceResponse()
        with response.gather(
            num_digits=1, action=reverse('topping'), method="POST"
        ) as g:
            g.say(message=message, loop=3)
        return Response(str(response),status =status.HTTP_200_OK,content_type='text/xml')


class Toppings(APIView):
    def post(self,request):
        """
            Handle menu items
        """
        crust_option = request.GET.get('Digits')
        #create the order
        order = Order.objects.create(crust=Crust.objects.get(size=int(crust_option)))
        #create message
        message = f"You have selected {order.crust.display_name} size."
        for i,topping in enumerate( Topping.objects.all() ):
            message += f"press {i+1} for {topping.name},"
            pass
        response = VoiceResponse()
        with response.gather(
            num_digits=1,
            action=reverse('finalize',kwargs={"order_id":order.id}),
            method="POST"
        ) as g:
            g.say(message=message, loop=3)


        return Response(str(response),status =status.HTTP_200_OK,content_type='text/xml')

        # return self._redirect_welcome()

class FinalizeOrder(APIView):

    def post(self,request,order_id):
        topping_option = request.GET.get('Digits')
        topping = Topping.objects.all()[int(topping_option)-1]
        #the order
        order = Order.objects.get(id=order_id)
        order.topping = topping
        order.draft = False
        order.save()
        #pricing
        total = order.crust.price + order.topping.price
        message = f"Your order for {order.crust.display_name} {order.topping.name} Pizza has been made successfully."
        message += f"Order ID is {order.id},"
        message += f"Total price is {total},Thank you for choosing PyPizza"
        # Start our TwiML response
        resp = VoiceResponse()
        # Read a message aloud to the caller
        resp.say(message, voice='Polly.Amy')
        return Response(str(resp),status =status.HTTP_200_OK,content_type='text/xml')
