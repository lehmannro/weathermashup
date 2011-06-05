from datetime import datetime, time, timedelta
import json
import urllib2

APIKEY = "30c8508a80203111110406"  # this is totally a trashmail account

def source(location):
    """
    :location: - city[,country]
               - zipcode
               - IP address
               - lat,lon (both in decimal degrees)

    """
    # format can also be XML or CSV
    uri = ("http://free.worldweatheronline.com/feed/weather.ashx"
           "?q=%s&format=json&num_of_days=5&key=%s"
           % (location, APIKEY))
    info = json.loads(urllib2.urlopen(uri).read())['data']
    if info.get('error'):
        return
    cur = info['current_condition'][0] # I'm unsure why this is a list at all
    obs = datetime.combine(datetime.today(),
            datetime.strptime(cur['observation_time'], '%H:%M %p').time())
    if obs < datetime.now():
        obs -= timedelta(days=1)
    yield dict(
        time_from = obs,
        time_to = obs + timedelta(seconds=1),
        temperature_current = float(cur['temp_C']),
        condition = cur['weatherDesc'][0]['value'],
        precipitation_amount = float(cur['precipMM']),
        wind_speed = float(cur['windspeedKmph']),
        wind_direction = cur['winddir16Point'],
    )
    for forecast in info['weather']:
        yield dict(
            time_from = datetime.strptime(forecast['date'], '%Y-%m-%d'),
            time_to = datetime.strptime(forecast['date'], '%Y-%m-%d'),
            temperature_min = float(forecast['tempMinC']),
            temperature_max = float(forecast['tempMaxC']),
            condition = forecast['weatherDesc'][0]['value'],
            precipitation_amount = float(forecast['precipMM']),
            wind_speed = float(forecast['windspeedKmph']),
            wind_direction = forecast['winddir16Point'],
        )
