from datetime import datetime, time, timedelta
import json
import urllib2
from lxml import etree

APIKEY = "IilKTBPV34FFCty0KvG9L1fEvNrynoReDhseuMv9nFli.w4KhN05cX3A1Tdhy5u0"  # this is totally a trashmail account

YAHOO_CONDITION_CODES = {
	'0': 'tornado',
	'1': 'tropical storm',
	'2': 'hurricane',
	'3': 'severe thunderstorms',
	'4': 'thunderstorms',
	'5': 'mixed rain and snow',
	'6': 'mixed rain and sleet',
	'7': 'mixed snow and sleet',
	'8': 'freezing drizzle',
	'9': 'drizzle',
	'10': 'freezing rain',
	'11': 'showers',
	'12': 'showers',
	'13': 'snow flurries',
	'14': 'light snow showers',
	'15': 'blowing snow',
	'16': 'snow',
	'17': 'hail',
	'18': 'sleet',
	'19': 'dust',
	'20': 'foggy',
	'21': 'haze',
	'22': 'smoky',
	'23': 'blustery',
	'24': 'windy',
	'25': 'cold',
	'26': 'cloudy',
	'27': 'mostly cloudy (night)',
	'28': 'mostly cloudy (day)',
	'29': 'partly cloudy (night)',
	'30': 'partly cloudy (day)',
	'31': 'clear (night)',
	'32': 'sunny',
	'33': 'fair (night)',
	'34': 'fair (day)',
	'35': 'mixed rain and hail',
	'36': 'hot',
	'37': 'isolated thunderstorms',
	'38': 'scattered thunderstorms',
	'39': 'scattered thunderstorms',
	'40': 'scattered showers',
	'41': 'heavy snow',
	'42': 'scattered snow showers',
	'43': 'heavy snow',
	'44': 'partly cloudy',
	'45': 'thundershowers',
	'46': 'snow showers',
	'47': 'isolated thundershowers',
	'3200': 'not available',
}

WIND_DIRECTIONS = {
    '0.0': 'N  ',
    '22.5': 'NNE',
    '45.0': 'NE ',
    '67.5': 'ENE',
    '90.0': 'E  ',
    '112.5': 'ESE',
    '135.0': 'SE ',
    '157.5': 'SSE',
    '180.0': 'S  ',
    '202.5': 'SSW',
    '225.0': 'SW',
    '247.5': 'WSW',
    '270.0': 'W  ',
    '292.5': 'WNW',
    '315.0': 'NW',
    '337.5': 'NNW',
    '360.0': 'N  ',
}



def source(location):
    """
    :location: - city[,country]
               - zipcode
               - lat,lon (both in decimal degrees)

    """
    # retrieve 'where-on-earth' ID; format can also be XML
    uri = "http://where.yahooapis.com/v1/places.q(%s)?format=json&appid=%s" % (location, APIKEY)
    info = json.loads(urllib2.urlopen(uri).read())['places']

    # take the first best place
    uri = "http://weather.yahooapis.com/forecastrss?w=%s&u=c" % info['place'][0]['woeid']
    info = etree.parse(uri)
    ns = 'http://xml.weather.yahoo.com/ns/rss/1.0'
    cond_date = info.findall("//{%s}condition" % ns)[0].get('date')
    cond_date = datetime.strptime(cond_date.rsplit(' ', 1)[0], '%a, %d %b %Y %I:%M %p')
    try:
        condition = YAHOO_CONDITION_CODES[info.findall("//{%s}condition" % ns)[0].get('code')]
    except KeyError:
        condition = info.findall("//{%s}condition" % ns)[0].get('text')
    sunrise_time = datetime.strptime(info.findall("//{%s}astronomy" % ns)[0].get('sunrise'), '%I:%M %p')
    sunrise_time = datetime.combine(cond_date.date(), sunrise_time.time())
    sunset_time = datetime.strptime(info.findall("//{%s}astronomy" % ns)[0].get('sunset'), '%I:%M %p')
    sunset_time = datetime.combine(cond_date.date(), sunset_time.time())
    # break down into WIND_DIRECTIONS
    wind_direction = WIND_DIRECTIONS[str(int(info.findall("//{%s}wind" % ns)[0].get('direction')) // 22.5 * 22.5)]

    data = [{
        'time_from': cond_date,
        'time_to': cond_date,
        'temperature_current': float(info.findall("//{%s}condition" % ns)[0].get('temp')),
        'wind_direction': wind_direction,
        'wind_speed': float(info.findall("//{%s}wind" % ns)[0].get('speed')),
        'condition': condition,
        'precipitation_probability': None,
        'precipitation_amount': None,
        'humidity': float(info.findall("//{%s}atmosphere" % ns)[0].get('humidity')),
        'sunrise_time': sunrise_time,
        'sunset_time': sunset_time,
        'warnings': None,
    }]

    for forecast in info.findall("//{%s}forecast" % ns):
        try:
            condition = YAHOO_CONDITION_CODES[forecast.get('code')]
        except KeyError:
            condition = forecast.get('text')
        time_from = datetime.strptime(forecast.get('date'), '%d %b %Y')
        time_to = datetime.combine(time_from.date(), datetime.strptime('23:59', '%H:%M').time())
        data.append({
            'time_from': time_from,
            'time_to': time_to,
            'temperature_min': float(forecast.get('low')),
            'temperature_max': float(forecast.get('high')),
            'condition': condition,
        })
    return data


if __name__ == '__main__':
    print source('berlin,germany')
