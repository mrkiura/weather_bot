from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse

from .query_weather import get_weather, generate_weather_message
from django.conf import settings


OPEN_WEATHER_API_KEY = settings.OPEN_WEATHER_API_KEY


@csrf_exempt
def webhook(request):
    response = MessagingResponse()
    if request.method == "POST":
        lat, lon = request.POST.get('Latitude'), request.POST.get('Longitude')
        if lat and lon:
            weather_response = get_weather(lat, lon, OPEN_WEATHER_API_KEY)
            message_body = generate_weather_message(weather_response)
            response.message(message_body)
        else:
            response.message("Send us your location")

    return HttpResponse(response.to_xml(), content_type='text/xml')
