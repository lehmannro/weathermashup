from datetime import datetime, timedelta

#{
#    //forecast: boolean;
#    time_from: datetime, 
#    time_to: datetime,
#    temperature_min: float in celsius,
#    temperature_max: float in celsius,
#    temperature_current: float in celsius,
#    wind_direction: string "NNE" len()==3 // NESW
#    wind_speed: float in km/h,
#    condition: ENUM [], // http://developer.yahoo.com/weather/#codes
#    precipitation_probability: float,
#    precipitation_amount: mm,
#    humiditiy: float,
#    sunrise_time: datetime,
#    sunset_time: datetime,
#    warnings: [string]
#}

def timedelta2seconds(delta):
    """ Convert a given timedelta to a number of seconds """
    return delta.microseconds / 1000000.0 \
           + delta.seconds + delta.days * 60*60*24 

def validate_report(report):
    assert isinstance(report['time_from'], datetime), report
    assert isinstance(report['time_to'], datetime), report

def reports_time_series(reports):
    now = datetime.now()
    last_dt = datetime.now()
    time_series = []
    for report in reports:
        validate_report(report)
        cur_dt = max(now, report['time_from'])
        time_delta = timedelta2seconds(cur_dt - last_dt)
        value_diffs = {
            'temperature_max': value_diff(report, reports,
                lambda k: k.get('temperature_max', k.get('temperature_current'))),
            'temperature_min': value_diff(report, reports,
                lambda k: k.get('temperature_min', k.get('temperature_current'))),
            'humiditiy': value_diff(report, reports,
                lambda k: k.get('humiditiy')),
            'precipitation_amount': value_diff(report, reports,
                lambda k: k.get('precipitation_amount')),
            'wind_speed': value_diff(report, reports,
                lambda k: k.get('wind_speed')),
            }
        series_item = {
            'time_delta': time_delta,
            'report': report,
            'value_diffs': value_diffs,
            }
        time_series.append(series_item)
    return time_series

def value_diff(report, reports, key_func, samples=3):
    if not key_func(report):
        return 0
    value = 0
    weights = 0
    for r in reports:
        time_d = abs(timedelta2seconds(report['time_from'] - r['time_from']))
        weight = 1/max(1, time_d)
        if key_func(r):
            weights += weight
            value += key_func(r)*weight
    return key_func(report) - (value/max(1, weights))


