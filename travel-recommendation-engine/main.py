from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__, static_folder="static", template_folder="templates")

COUNTRIES_API = "https://restcountries.com/v3.1"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def random_country():
    try:
        response = requests.get(f"{COUNTRIES_API}/all")
        countries = response.json()
        country = random.choice(countries)
        return jsonify({
            "country": country["name"]["common"],
            "capital": country.get("capital", ["N/A"])[0],
            "population": f"{country.get('population', 0):,}",
            "languages": ", ".join(country.get("languages", {}).values()) if country.get("languages") else "N/A",
            "flag": country.get("flags", {}).get("png", "")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/country/<name>")
def get_country(name):
    try:
        response = requests.get(f"{COUNTRIES_API}/name/{name}")
        country = response.json()[0]
        return jsonify({
            "country": country["name"]["common"],
            "capital": country.get("capital", ["N/A"])[0],
            "population": f"{country.get('population', 0):,}",
            "languages": ", ".join(country.get("languages", {}).values()) if country.get("languages") else "N/A",
            "flag": country.get("flags", {}).get("png", "")
        })
    except:
        return jsonify({"error": "Country not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
