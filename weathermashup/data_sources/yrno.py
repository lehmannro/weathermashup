from datetime import datetime

from geopy import geocoders
from lxml import etree

def parse_time(time_string):
    return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')

def mps_to_kmh(mps_value):
    return float(mps_value) * 3.6

def normalize(value):
    return float(value)/100

def find_weather(location):
    yrno_url = "http://api.yr.no/weatherapi/locationforecast/1.8/?lat=%(lat)s;lon=%(lon)s"

    place, (lat, lng) = geocoders.Google().geocode(location)

    url = yrno_url % { 'lat': lat, 'lon': lng}

    tree = etree.parse(url)

    for time in tree.xpath("//product/time"):
        entry = dict (
            time_from=parse_time(time.attrib['from']),
            time_to=parse_time(time.attrib['from'])
        )
        mapping = dict(
            temperature=('value', float, 'temperature_current'),
            windDirection=('name', None, 'wind_direction'),
            windSpeed=('mps', mps_to_kmh, 'wind_speed'),
            precipitation=('value', float, 'precipitation_amount'),
            humidity=('value', normalize, 'humidity'),
        )

        for i in time[0]:
            if mapping.has_key(i.tag):
                (attr, func, entry_key) = mapping[i.tag]
                if func:
                    entry[entry_key] = func(i.attrib[attr])
                else:
                    entry[entry_key] = i.attrib[attr]
        yield entry

if __name__ == "__main__":
    import sys
    from pprint import pprint
    pprint(list(find_weather(sys.argv[1])))
    
    
    