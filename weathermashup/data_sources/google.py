import pywapi
from datetime import datetime, timedelta

def fahrenheit(s): # -> celsius
    return (float(s) - 32) * 5. / 9

def mph(s): # -> kmh
    return float(s) * 1.609344

def source(location):
    info = pywapi.get_weather_from_google(location)
    if not info['forecast_information']:
        return
    assert info['forecast_information']['unit_system'] == 'US'

    cur = info['current_conditions']
    start = datetime.strptime(
        info['forecast_information']['current_date_time'].rsplit(None, 1)[0],
        '%Y-%m-%d %H:%M:%S')
    yield dict(
        time_from = start,
        time_to = start + timedelta(seconds=1),
        temperature_current = float(cur['temp_c']),
        wind_direction = cur['wind_condition'].split()[1],
        wind_speed = mph(cur['wind_condition'].split()[3]),
        condition = cur['condition'],
        humidity = float(cur['humidity'].split()[1].rstrip('%')),
    )

    # let's hope they are ordered
    for day, forecast in enumerate(info['forecasts']):
        yield dict(
            time_from = start.replace(hour=0, minute=0) + timedelta(days=day),
            time_to = (start + timedelta(days=day)).replace(hour=0, minute=0),
            condition = forecast['condition'],
            temperature_min = fahrenheit(forecast['low']),
            temperature_max = fahrenheit(forecast['high']),
        )
