from datetime import datetime, timedelta

from geopy import geocoders
from lxml import etree

def parse_time(time_string):
    return datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')

def mps_to_kmh(mps_value):
    return float(mps_value) * 3.6

XML_MAPPING = dict(
    temperature=('value', float, 'temperature_current'),
    windDirection=('name', None, 'wind_direction'),
    windSpeed=('mps', mps_to_kmh, 'wind_speed'),
    precipitation=('value', float, 'precipitation_amount'),
    humidity=('value', float, 'humidity'),
)


def find_weather(location):
    place, (lat, lng) = geocoders.Google().geocode(location)
    
    yrno_url = "http://api.yr.no/weatherapi/locationforecast/1.8/?lat=%(lat)s;lon=%(lon)s"
    url = yrno_url % { 'lat': lat, 'lon': lng}
    tree = etree.parse(url)
    last_time_diff = timedelta(0)

    for time in tree.xpath("//product/time"):
        entry = dict (
            time_from=parse_time(time.attrib['from']),
            time_to=parse_time(time.attrib['to'])
        )
        
        # skip duplicate entries with bigger timeframe in an unclean way
        time_diff = entry['time_to'] - entry['time_from']
        if last_time_diff > timedelta(0) and \
           time_diff > last_time_diff:
            continue
        last_time_diff = time_diff
        
        for i in time[0]:
            if XML_MAPPING.has_key(i.tag):
                (attr, func, entry_key) = XML_MAPPING[i.tag]
                if func:
                    entry[entry_key] = func(i.attrib[attr])
                else:
                    entry[entry_key] = i.attrib[attr]
        yield entry

if __name__ == "__main__":
    import sys
    from pprint import pprint
    pprint(list(find_weather(sys.argv[1])))
