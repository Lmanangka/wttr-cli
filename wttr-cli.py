'''
Author: Leonardo Rudolf Manangka
Created: 19 January 2023
'''
import argparse
import json
import sys
import re
from tabulate import tabulate
from datetime import datetime
from configparser import ConfigParser
from urllib import parse, error, request

BASE_CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_WEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def _get_api_key():
    config = ConfigParser()
    config.read("api_key.ini")
    return config["openweather"]["api_key"]

def read_usr_input():
    parser = argparse.ArgumentParser(prog="wttr-cli",
                                     description="wttr-cli is an app to display\
                                             a current weather and weather\
                                             forecast.",
                                     epilog="Example: python wttr-cli semarang")
    parser.add_argument("city", nargs='+', type=str, help="enter a city name")
    parser.add_argument("-f", "--forecast", action="store_true",
                        help="show weather forecast with 3 hours interval")
    parser.add_argument("-l", "--lang", nargs=1, type=str, default="en",
                        help="show weather with your chosen language")
    return parser.parse_args()

def build_weather_query(city_name, language, forecast=False):
    api_key = _get_api_key()
    city = " ".join(city_name)
    encode_city = parse.quote_plus(city)
    encode_lang = language[0]
    url = (f"{BASE_WEATHER_FORECAST_URL}?q={encode_city}&cnt=24&appid={api_key}"
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
    # realtime date time using library time
    timeNow = datetime.now()
    compNow = [timeNow.day, timeNow.hour]
    # created new dictionary for data forecast from API
    data = {'City': [], 'Temperature': [], 'Weather': [],
            'Description': [], 'Time': []}
    if 'list' in wttr_data:
        for tmp in wttr_data['list']:
            # filter date time, and stored it in a list [date, time]
            dateFiltered = re.split(' |-|:|0', tmp['dt_txt'])
            dateFiltered = list(filter(None, dateFiltered))
            del dateFiltered[0:3]
            dateFiltered = [eval(i) for i in dateFiltered]
            dateFiltered.append(0) if len(dateFiltered) < 2 else dateFiltered
            # compare date time today and forecast date the output will be
            # 3 days forecast including today with 3 hours intervals
            if dateFiltered >= compNow:
                data['City'].append(city)
                data['Temperature'].append(tmp['main']['temp'])
                data['Weather'].append(tmp['weather'][0]['main'])
                data['Description'].append(tmp['weather'][0]['main'])
                data['Time'].append(tmp['dt_txt'])
        # make a table using tabulate read data from data dictionary
        print(tabulate(data, headers='keys', tablefmt='fancy_grid'))
    else:
        data['City'].append(city)
        data['Temperature'].append(wttr_data['main']['temp'])
        data['Weather'].append(wttr_data['weather'][0]['main'])
        data['Description'].append(wttr_data['weather'][0]['main'])
        data['Time'].append(str(timeNow).split('.')[:-1][0])
        print(tabulate(data, headers='keys', tablefmt='fancy_grid'))

if __name__ == "__main__":
    usr_input = read_usr_input()
    wttr_query = build_weather_query(usr_input.city, usr_input.lang,
                                     usr_input.forecast)
    wttr_data = get_data(wttr_query)
    display_data(wttr_data)

