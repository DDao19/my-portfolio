from flask import Flask, render_template, request
from pathlib import Path
import csv

app = Flask(__name__)
csv_path = Path("database.csv")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<string:url_route>")
def routes(url_route):
    try:
        return render_template(f"{url_route}")
    except:
        return render_template("404.html"), 404


def write_to_csv(data):

    with open(csv_path, mode="a", newline="") as database:
        field_keys = list(data.keys())
        writer = csv.DictWriter(database, fieldnames=field_keys)

        if csv_path.stat().st_size == 0:  # Check if the csv file is empty
            writer.writeheader()
            writer.writerow(data)
        else:
            writer.writerow(data)


@app.route("/form_submit", methods=["POST", "GET"])
def form_submit():
    if request.method == "POST":
        try:
            form_data = request.form.to_dict()
            write_to_csv(form_data)

            return render_template("thank-you.html")
        except Exception as e:
            print(f"Error writing to CSV: {e}")
            return "Oops! Something went wrong. Please try again."

    return render_template("thank-you.html")
