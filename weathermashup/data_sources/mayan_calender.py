from datetime import datetime

def armageddon(location):
    if location.lower().strip() == 'bielefeld':
        return []
    return [{
        "time_from": datetime(2012, 12, 12),
        "temperature_max": 999999999,
        "temperature_min": 999999998,
        "time_to": "end of time", #datetime(2999, 1, 1),
        "warnings": ["Mayan Calendar claims armageddon. Don't plan vacations after this."]
        }]
