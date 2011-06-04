import pywapi

def scraper(location):
    info = pywapi.get_weather_from_google(location)

    cur = info['current_conditions']
    yield {
        time_from: info['forecast_information']['current_date_time'],
        time_to: info['forecast_information']['current_date_time']
                 + datetime.timedelta(days=1),
        temperature_current: cur['temp_c'],
        wind_direction: cur['wind_condition'].split()[1],
        wind_speed: float(cur['wind_condition'].split()), #XXX mph
        condition: cur['condition'],
        humidity: float(cur['humidity'].split()[1]),
    }

    for forecast in info['forecasts']:
        yield {
            condition: forecast['condition'],
            temperature_min: forecast['low'],
            temperature_max: forecast['high'],
        }
