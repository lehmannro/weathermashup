from flask import Flask, render_template, request
from lookup import reports_by_location
from logic import reports_time_series
from jinja2 import evalcontextfilter

from collections import defaultdict
from datetime import datetime
import json

app = Flask(__name__)


COLORS = dict(
    metar="#edc240",
    wwo="#afd8f8",
    google="#cb4b4b",
    yrno="#4da74d",
    wetter_com="#9440ed"
)

def json_types(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%s")
    raise TypeError()

def to_json(obj):
    return json.dumps(obj, default=json_types, indent=2)

@app.template_filter()
@evalcontextfilter
def datetimeformat(ctx, value, format='%A, %H:%M'):
    return value.strftime(format)

@app.route("/")
def index(input_warning=None):
    return render_template("index.html",
            input_warning=input_warning)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/timeline")
def timeline():
    location = request.args.get('location')
    if not location or len(location) < 3:
        return index(input_warning="Bitte gib einen Ort ein!")

    reports = reports_by_location(location)
    time_series = reports_time_series(reports)
    time_series_json = to_json(time_series)

    grouped_by_source = {}
    grouped_by_timeslot = [(0, {})]
    for entry in time_series:
        source = entry['report']['source']
        if not grouped_by_source.has_key(source):
            grouped_by_source[source] = [entry]
        else:
            grouped_by_source[source].append(entry)

        slot = entry['report']['time_from']
        # bucket into 3-hour time slots
        slot = slot.replace(hour=slot.hour // 3 * 3, minute=0)
        if slot != grouped_by_timeslot[-1][0]:
            grouped_by_timeslot.append((slot, defaultdict(dict)))

        #XXX currently, the last item in a slot always wins. this no good.
        merger = grouped_by_timeslot[-1][1][entry['report']['source']]
        merger.update(entry['report'])
    grouped_by_timeslot.pop(0)

    plot_data = []
    for source_name, source in grouped_by_source.iteritems():
        temps_min = []
        temps_max = []
        precipitation_list = []

        for entry in source:
            report = entry['report']
            time = int(report['time_from'].strftime("%s"))*1000
            if report.has_key('precipitation_amount'):
                precipitation_list.append((time, report['precipitation_amount']))
            if 'temperature_current' in report:
                temps_min.append((time, report['temperature_current']))
                temps_max.append((time, report['temperature_current']))
            else:
                if 'temperature_min' in report:
                    temps_min.append((time, report['temperature_min']))
                if 'temperature_max' in report:
                    temps_max.append((time, report['temperature_max']))

        plot_data.append(dict(id=source_name,
                              label=source_name,
                              data=temps_min,
                              color=COLORS[source_name]))
        plot_data.append(dict(data=temps_max,
                              color=COLORS[source_name],
                              fillBetween=source_name,
                              lines=dict(fill=True)))

        if precipitation_list:
            plot_data.append(dict(data=precipitation_list,
                                  bars=dict(show=True),
                                  color=COLORS[source_name],
                                  yaxis=2))

    return render_template("timeline.html",
            location=location,
            grouped_by_source=grouped_by_source,
            grouped_by_timeslot=grouped_by_timeslot,
            plot_data=to_json(plot_data))


if __name__ == "__main__":
    app.debug = True
    app.run()
