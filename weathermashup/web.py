from flask import Flask, render_template, request
from lookup import reports_by_location
app = Flask(__name__)

@app.route("/")
def index(input_warning=None):
    return render_template("index.html",
            input_warning=input_warning)

@app.route("/timeline")
def timeline():
    location = request.args.get('location')
    if not location or len(location) < 3:
        return index(input_warning="Bitte gib einen Ort ein!")

    return render_template("timeline.html", 
            reports=reports_by_location(location))


if __name__ == "__main__":
    app.debug = True
    app.run()

