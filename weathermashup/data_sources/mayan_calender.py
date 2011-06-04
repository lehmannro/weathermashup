from datetime import datetime

def armageddon(location):
    if location.lower().strip() == 'bielefeld':
        return []
    return [{
        "time_from": datetime(2012, 12, 12),
        "time_to": datetime.max,
        "temperature_max": 999999999,
        "temperature_min": 999999998,
        "warnings": ["Mayan Calendar claims armageddon. Don't plan vacations after this."]
        }]
