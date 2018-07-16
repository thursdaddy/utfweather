#!/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
from configparser import ConfigParser
import argparse
import logging
import time

logging.getLogger().setLevel(logging.WARNING)


def icons_to_unicode(icon_code):
    switcher = {
        # Day icon	Night icon	Description
        # 01d.png  	01n.png  	clear sky 🌣
        "01d": "🌣",
        "01n": "🌣",
        # 02d.png  	02n.png  	few clouds 🌤
        "02d": "🌤",
        "02n": "🌤",
        # 03d.png  	03n.png  	scattered clouds 🌥
        "03d": "🌤",
        "03n": "🌤",
        # 04d.png  	04n.png  	broken clouds 🌥
        "04d": "🌥",
        "04n": "🌥",
        # 09d.png  	09n.png  	shower rain 🌦
        "09d": "🌦",
        "09n": "🌦",
        # 10d.png  	10n.png  	rain 🌦
        "10d": "🌦",
        "10n": "🌦",
        # 11d.png  	11n.png  	thunderstorm 🌩
        "11d": "🌩",
        "11n": "🌩",
        # 13d.png  	13n.png  	snow 🌨
        "13d": "🌨",
        "13n": "🌨",
        # 50d.png  	50n.png  	mist 🌫
        "50d": "🌫",
        "50n": "🌫",
    }
    return str(switcher.get(icon_code, "nothing"))


def get_weather(config):
    if config['forecast_type'] == "daily":
        # Request weather data from openweathermap.org. Returns request object with JSON string in r.text.
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=" + config['zip_code'] + "&APPID=" + config['api_key'] + "&units=" + config['units'])

        # Parse JSON
        weather = json.loads(r.text)

        info = weather["weather"][0]["description"].title()
        temp = int(weather["main"]["temp"])
        icon = icons_to_unicode(weather["weather"][0]["icon"])

        result = icon + " " + info + "  🌡 " + str(temp) + "°" + config['unit_key']

    elif config['forecast_type'] == "5day":
        result = "Waiting on Jake to do the 5 day forecast"

    with open(cache_path, 'w') as cache_file:
        logging.debug("Writing cache.")
        cache_file.write(result)
    return result


# Add options and parse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--toggle-forecast", help="Toggle Between 5day and Current Weather", action="store_true")
parser.add_argument("-v", "--verbose", help="Enable Verbose Logging", action="store_true")
args = parser.parse_args()

if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

home_dir = os.getenv("HOME")
config_path = home_dir + '/.config/utfweather/utfweather.conf'
cache_path = home_dir + "/.cache/utfweather/utfweather.cache"

# Load the configuration file
cp = ConfigParser()
cp.read(config_path)

logging.debug("Loaded the following settings:")
logging.debug(dict(cp.items('general')))

config = {'forecast_type': cp.get('general', 'forecast_type'),
          'zip_code': cp.get('general', 'zip_code'),
          'api_key': cp.get('general', 'api_key'),
          'units': cp.get('general', 'units'),
          'unit_key': cp.get('general', 'unit_key'),
          'cache_ageout': cp.get('general', 'cache_ageout')}

# Toggle forecast type
if args.toggle_forecast:
    if config['forecast_type'] == "daily":
        config['forecast_type'] = "5day"
        cp.set('general', 'forecast_type', "5day")
    elif config['forecast_type'] == "5day":
        config['forecast_type'] = "daily"
        cp.set('general', 'forecast_type', "daily")

    logging.debug("Writing the following settings:")
    logging.debug(dict(cp.items('general')))

    with open(config_path, 'w') as config_file:
        cp.write(config_file)

    get_weather(config)

else:
    # CHeck if cache exists and is current
    if os.path.exists(cache_path):
        mod_time = os.stat(cache_path).st_mtime
        current_time = int(time.time())
        cache_age = current_time - mod_time

        logging.debug("Mod Time: " + str(mod_time))
        logging.debug("Current Time:" + str(current_time))
        logging.debug("Cache Age:" + str(cache_age))

        if cache_age > int(config["cache_ageout"]):
            logging.debug("Cache old... Getting current weather.")
            result = get_weather(config)

        # Write cache
        else:
            with open(cache_path, 'r') as cache_file:
                logging.debug("Reading cache.")
                result = cache_file.read()

    # If cache doesnt exist run get_weather
    else:
        result = get_weather(config)

    print(result)
