import calendar
from datetime import datetime

import requests


def get_weather(lat, lon, api_key):
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat"
        f"={lat}&lon={lon}&exclude=hourly&appid={api_key}&"
        f"units=metric").json()
    return weather_response


def generate_weather_message(weather_response):
    current_weather = {
        "temperature": int(weather_response["current"]["temp"]),
        "day_of_week": calendar.day_name[datetime.fromtimestamp(
            weather_response["current"]["dt"]).weekday()],
        "description":
            weather_response["current"]["weather"][0]["description"],
        "main":
            weather_response["current"]["weather"][0]["main"]
    }

    forecast_messages = []
    for daily_weather in weather_response["daily"]:
        max_temp = daily_weather["temp"]["max"]
        min_temp = daily_weather["temp"]["min"]
        weekday = calendar.day_name[datetime.fromtimestamp(
            daily_weather["dt"]).weekday()]
        description = daily_weather["weather"][0]["description"]
        forecast_message = f"{weekday}: {description}, " \
                           f"Low {min_temp}℃, High {max_temp}℃  \n"
        forecast_messages.append(forecast_message)
    forecast_messages = "\n".join(forecast_messages)
    message_body = f" *Current Weather* \n \n"\
                   f"{current_weather['day_of_week']}: "\
                   f"{current_weather['description']}, "\
                   f"{current_weather['temperature']} ℃ \n \n"\
                   f" *Forecast* \n \n"\
                   f"{forecast_messages}"

    return message_body
