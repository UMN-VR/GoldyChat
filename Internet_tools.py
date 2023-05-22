import datetime
import requests

def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_geolocation():
    response = requests.get('https://ipapi.co/json/')
    data = response.json()
    return data['city'], data['region'], data['country']
