from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from twilio.twiml.voice_response import VoiceResponse

class AnswerCall(APIView):
    def get(self, request):
        """Respond to incoming phone calls with a brief message."""
        # Start our TwiML response
        resp = VoiceResponse()

        # Read a message aloud to the caller
        resp.say("Thank you for calling! Have a great day.", voice='Polly.Amy')

        return Response(str(resp),status =status.HTTP_200_OK)

    def post(self, request):
        """Respond to incoming phone calls with a brief message."""
        # Start our TwiML response
        resp = VoiceResponse()

        # Read a message aloud to the caller
        resp.say("Thank you for calling! Have a great day.", voice='Polly.Amy')

        return Response(str(resp),status =status.HTTP_200_OK)
