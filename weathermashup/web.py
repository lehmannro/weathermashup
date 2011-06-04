from flask import Flask, render_template, request
from lookup import reports_by_location
from logic import reports_time_series

from datetime import datetime
import json 

app = Flask(__name__)

def json_types(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%s")
    raise TypeError()

def to_json(obj):
    return json.dumps(obj, default=json_types, indent=2)

@app.route("/")
def index(input_warning=None):
    return render_template("index.html",
            input_warning=input_warning)

@app.route("/timeline")
def timeline():
    location = request.args.get('location')
    if not location or len(location) < 3:
        return index(input_warning="Bitte gib einen Ort ein!")

    reports = reports_by_location(location)
    time_series = reports_time_series(reports)
    time_series_json = to_json(time_series)
    # import pdb; pdb.set_trace()
    grouped_by_source = {}
    for entry in time_series:
        source = entry['report']['source']
        if not grouped_by_source.has_key(source):
            grouped_by_source[source] = [entry]
        else:
            grouped_by_source[source].append(entry)

    return render_template("timeline.html", 
            location=location,
            grouped_by_source=grouped_by_source)


if __name__ == "__main__":
    app.debug = True
    app.run()

