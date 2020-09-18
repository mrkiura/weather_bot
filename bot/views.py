from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client

from .query_weather import get_weather, generate_weather_message
from django.conf import settings


TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
OPEN_WEATHER_API_KEY = settings.OPEN_WEATHER_API_KEY
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@csrf_exempt
def webhook(request):

    if request.method == "POST":
        lat, lon = request.POST.get('Latitude'), request.POST.get('Longitude')
        if lat and lon:
            weather_response = get_weather(lat, lon, OPEN_WEATHER_API_KEY)
            message_body = generate_weather_message(weather_response)
            recipient_number = request.POST.get("From")
            bot_number = request.POST.get("To")

            message = TWILIO_CLIENT.messages.create(
                body=message_body,
                from_=bot_number,
                to=recipient_number
            )

    return JsonResponse({"Status": "Message Received"})
