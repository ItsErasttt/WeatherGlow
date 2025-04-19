from flask import Flask, render_template, request
import requests
import config
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = request.form.get("city", "Москва")  

    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"]
            }

    return render_template("index.html", weather=weather_data, city=city)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))