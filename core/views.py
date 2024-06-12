from django.shortcuts import render
import requests, datetime
from weather_app import settings


def index(request):
    if "city" in request.POST:
        city = request.POST["city"]
    else:
        city = "Nairobi"
    API_KEY = settings.DJANGO_OPEN_WEATHER_APP_API_KEY
    URL = "https://api.openweathermap.org/data/2.5/forecast"
    PARAMS = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(url=URL, params=PARAMS)
    res = r.json()
    city = res["city"]["name"]
    country = res["city"]["country"]
    temp = res["list"][0]["main"]["feels_like"]
    days = []
    for i in range(0, 40, 8):
        daily_weather = {
            "temp": res["list"][i]["main"]["feels_like"],
            "weather": res["list"][i]["weather"][0]["main"],
            "weather_description": res["list"][i]["weather"][0]["description"],
            "weather_icon": res["list"][i]["weather"][0]["icon"],
            "dt": datetime.datetime.strptime(res["list"][i]["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%A, %B %d, %Y %I:%M %p"),
        }
        days.append(daily_weather)
    context = {"city": city, "country": country, "temp": temp, "days": days}
    return render(request, "core/index.html", context)
