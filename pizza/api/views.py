from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from twilio.twiml.voice_response import VoiceResponse

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
        response = VoiceResponse()
        with response.gather(
            num_digits=1, action=reverse('menu'), method="POST"
        ) as g:
            g.say(
                message="Thanks for calling the E T Phone Home Service. " +
                  "Please press 1 for directions." +
                  "Press 2 for a list of planets to call.", loop=3)

        return Response(str(response),status =status.HTTP_200_OK,content_type='text/xml')


class Menu(APIView):
    # private methods
    def _give_instructions(self,response):
        response.say("To get to your extraction point, get on your bike and go " +
                     "down the street. Then Left down an alley. Avoid the police" +
                     " cars. Turn left into an unfinished housing development." +
                     "Fly over the roadblock. Go past the moon. Soon after " +
                     "you will see your mother ship.",
                     voice="Polly.Amy", language="en-GB")

        response.say("Thank you for calling the E T Phone Home Service - the " +
                     "adventurous alien's first choice in intergalactic travel")

        response.hangup()
        return response


    def _list_planets(self,response):
        with response.gather(numDigits=1, action=reverse('menu'), method="POST")\
        as g:
            g.say("To call the planet Broh doe As O G, press 2. To call the " +
                  "planet DuhGo bah, press 3. To call an oober asteroid " +
                  "to your location, press 4. To go back to the main menu " +
                  " press the star key.",
                  voice="Polly.Amy", language="en-GB", loop=3)

        return response


    def _redirect_welcome(self):
        response = VoiceResponse()
        response.say("Returning to the main menu", voice="Polly.Amy", language="en-GB")
        response.redirect(url_for('welcome'))

        return Response(str(response),status =status.HTTP_200_OK,content_type='text/xml')

    def post(self,request):
        """
            Handle menu items
        """
        selected_option = request.GET.get('Digits')
        print(selected_option)
        option_actions = {
            '1': self._give_instructions,
            '2': self._list_planets
        }

        if selected_option in option_actions:
            response = VoiceResponse()
            option_actions[selected_option](response)
            return Response(str(response),status =status.HTTP_200_OK,content_type='text/xml')

        return self._redirect_welcome()
