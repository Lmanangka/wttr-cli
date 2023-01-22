'''
Author: Leonardo Rudolf Manangka
Created: 19 January 2023
'''
import argparse
import json
import sys
from configparser import ConfigParser
from urllib import parse, error, request
from pprint import pp

BASE_CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_WEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def _get_api_key():
    config = ConfigParser()
    config.read("api_key.ini")
    return config["openweather"]["api_key"]

def read_usr_input():
    parser = argparse.ArgumentParser(prog="wttr",
                                     description="wttr is an app to display a\
                                             current weather and weather\
                                             forecast.")
    parser.add_argument("city", nargs='+', type=str, help="Enter a city name")
    parser.add_argument("-f", "--forecast", action="store_true",
                        help="Display weather forecast")
    parser.add_argument("-l", "--lang", nargs=1, type=str,
                        help="Display wttr with your chosen language")
    return parser.parse_args()

def build_weather_query(city_name, language, forecast=False):
    api_key = _get_api_key()
    city = " ".join(city_name)
    encode_city = parse.quote_plus(city)
    encode_lang = language = "en" if language is None else language[0]
    url = (f"{BASE_WEATHER_FORECAST_URL}?q={encode_city}&appid={api_key}"
    f"&units=metric&lang={encode_lang}") if forecast is True else (f""
    f"{BASE_CURRENT_WEATHER_URL}?q={encode_city}&appid={api_key}&units=metric"
    f"&lang={encode_lang}")
    return url

def get_data(wttr_query):
    try:
        resp = request.urlopen(wttr_query)
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("Access denied check your api_key!!")
        elif http_error.code == 404:
            sys.exit("Can't find this city name")
        else:
            sys.exit("Something went wrong...({http_error.code})")
    data = resp.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response!!")

def display_data(wttr_data):
    city = wttr_data['name'] if 'name' in wttr_data else wttr_data['city']['name']
    temperature = wttr_data['list'][0]
    print(temperature)

if __name__ == "__main__":
    usr_input = read_usr_input()
    wttr_query = build_weather_query(usr_input.city, usr_input.lang,
                                     usr_input.forecast)
    wttr_data = get_data(wttr_query)
#    print(usr_input)
#    print(wttr_query)
#    pp(wttr_data)
    display_data(wttr_data)

