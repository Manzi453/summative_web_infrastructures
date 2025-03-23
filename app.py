from flask import Flask, render_template, request
import requests

def create_app():
    app = Flask(__name__)

    # Replace with your OpenWeatherMap API key
    API_KEY = "9dfc06c1de34c33ab1b97f5fbb56813a"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

    @app.route("/", methods=["GET", "POST"])
    def index():
        weather_data = None
        forecast_data = None
        if request.method == "POST":
            city = request.form.get("city")
            print(f"City received: {city}")  # Debug print
            if city:
                weather_data = get_weather(city)
                print(f"Weather data: {weather_data}")  # Debug print
                forecast_data = get_forecast(city)
                print(f"Forecast data: {forecast_data}")  # Debug print
        return render_template("index.html", weather=weather_data, forecast=forecast_data)

    def get_weather(city):
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        print(f"Weather API error: {response.status_code}")  # Debug print
        return None

    def get_forecast(city):
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(FORECAST_URL, params=params)
        if response.status_code == 200:
            return response.json()
        print(f"Forecast API error: {response.status_code}")  # Debug print
        return None

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)