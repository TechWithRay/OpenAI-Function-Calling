import json
import requests
import logging
import argparse
from consts import WEATHER_API_KEY

parser = argparse.ArgumentParser()

parser.add_argument("--location", required=True, help="location of your city")


def get_current_weather(location, unit="Fahrenheit "):
    """
    Get the current weather in a given location
    """

    BASE_URL = (
        "https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}"
    )

    # change the unit for the api
    api_unit = "metric" if unit == "Celsius" else "imperial"

    # Hand edge case, e.g. Sunnyvale, CA
    location = location.split(",")[0] if "," in location else location

    url = BASE_URL.format(location, WEATHER_API_KEY, api_unit)

    response = requests.get(url)

    data = response.json()

    if data["cod"] == "404":
        raise RuntimeError("Cannot find this city, please retry!")

    weather_info = json.dumps(
        {
            "location": location,
            "temperature": data["main"]["temp"],
            "unit": unit,
        }
    )

    return weather_info


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO,
    )
    args = parser.parse_args()
    get_current_weather(args.location)
