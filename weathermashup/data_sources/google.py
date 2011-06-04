import pywapi
from datetime import datetime, timedelta

def source(location):
    info = pywapi.get_weather_from_google(location)
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
        wind_speed = float(cur['wind_condition'].split()[3]), #XXX mph
        condition = cur['condition'],
        humidity = float(cur['humidity'].split()[1].rstrip('%')),
    )

    # let's hope they are ordered
    for day, forecast in enumerate(info['forecasts']):
        yield dict(
            time_from = start.replace(hour=0, minute=0) + timedelta(days=day),
            time_to = (start + timedelta(days=day)).replace(hour=0, minute=0),
            condition = forecast['condition'],
            temperature_min = float(forecast['low']), #XXX fahrenheit
            temperature_max = float(forecast['high']),
        )
