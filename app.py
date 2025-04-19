import os
from flask import Flask, render_template, request
import requests

# Инициализация Flask приложения
app = Flask(__name__)

# Конфигурация (можно вынести в отдельный config.py)
app.config['API_KEY'] = os.environ.get('API_KEY', 'ваш_ключ_по_умолчанию')

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = request.form.get("city", "Москва")  # Город по умолчанию
    
    if city:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app.config['API_KEY']}&units=metric&lang=ru"
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            
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
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
        except (KeyError, ValueError) as e:
            print(f"Ошибка обработки данных: {e}")

    return render_template("index.html", weather=weather_data, city=city)

# Обработчик для страницы 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Точка входа (важно для Gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)