from django.urls import reverse
from rest_framework.views import APIView
from django.http import HttpResponse

from twilio.twiml.voice_response import VoiceResponse
from pizza.models import OrderMessageConfig,Crust,Order,Topping

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
        return HttpResponse(str(response),status=200,content_type='text/xml')


class Toppings(APIView):
    def post(self,request):
        """
            Handle menu items
        """
        crust_option = request.POST.get('Digits')
        phone_number = request.POST.get('Caller')
        #create the order
        order = Order.objects.create(
            crust=Crust.objects.get(size=int(crust_option)),
            phone_number = phone_number            
        )
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

        return HttpResponse(str(response),status=200,content_type='text/xml')


class FinalizeOrder(APIView):

    def post(self,request,order_id):
        topping_option = request.POST.get('Digits')
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
        return HttpResponse(str(resp),status=200,content_type='text/xml')
