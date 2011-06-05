from hashlib import md5
from datetime import datetime
#from urllib import urlopen
from lxml import etree

BASE_URL = 'http://api.wetter.com/'
#http://api.wetter.com/forecast/weather/city/<CityCode>/project/<Projektname>/cs/<Checksumme>

API_KEY = 'f03234052eed0ae87dcb2656e2fb7fc6'
PROJECT = 'weatherexperiment'

def build_search(location, query):
    csum = md5(PROJECT + API_KEY + query).hexdigest()
    url = BASE_URL + location + "/" + query + "/project/" + PROJECT + "/cs/" + csum
    return etree.parse(url)


def find(location):
    doc_name = build_search('location/index/search', location)
    code = doc_name.findtext('//result/item/city_code')
    doc_fcast = build_search('forecast/weather/city', code)
    forecasts = []
    for elem in doc_fcast.findall('//date/time'):
        ti = datetime.strptime(elem.findtext('dhl'), '%Y-%m-%d %H:%M')
        fcast = {
            'condition': elem.findtext('w_txt'),
            'wind_direction': elem.findtext('wd_txt'),
            'wind_speed': float(elem.findtext('ws')),
            'precipitation_probability': float(elem.findtext('ws')),
            'temperature_min': float(elem.findtext('tn')),
            'temperature_max': float(elem.findtext('tx')),
            'time_from': ti, 
            'time_to': ti
            }
        fcast['wind_direction'] = fcast['wind_direction'].upper().replace('O', 'E')
        forecasts.append(fcast)
    return forecasts


if __name__ == '__main__':
    from pprint import pprint
    forecasts = find('Berlin')
    pprint(forecasts)


