import os
from typing import Tuple, List
import requests
from dotenv import load_dotenv

geo_url = 'https://geocode-maps.yandex.ru/1.x/'
weather_url = 'https://api.weather.yandex.ru/v2/forecast'
load_dotenv()  # загрузка токенов


def get_weather_coordinates(city: str) -> Tuple[str, str]:
    payload: dict = {'apikey': os.getenv('GEO_KEY'), 'geocode': city,
                     'format': 'json'}
    data: dict = requests.get(geo_url, params=payload).json()
    _coords: dict = data['response']['GeoObjectCollection']["featureMember"][0]
    coords: List[str] = _coords["GeoObject"]["Point"]["pos"].split()
    return coords[0], coords[1]  # (широта, долгота)


def get_temp_info(lat, lon) -> dict:
    payload: dict = {'lat': lat, 'lon': lon, 'lang': 'ru_RU', 'format': 'json'}
    headers: dict = {'X-Yandex-API-Key': os.getenv('WEATHER_KEY')}
    data: dict = requests.get(weather_url, params=payload,
                              headers=headers).json()
    return data


if __name__ == "__main__":
    city: str = 'Москва'
    coords: Tuple[str, str] = get_weather_coordinates(city)
    lon, lat = coords
    print(get_temp_info(lat, lon))
