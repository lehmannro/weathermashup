from pkg_resources import iter_entry_points

ENTRY_POINT_GROUP = "weather.sources"

def reports_by_location(location):
    reports = []
    for ep in iter_entry_points(ENTRY_POINT_GROUP):
        func = ep.load()
        reports.extend(func(location))
    return reports


