import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO


# ============================================================
# API URLS
# ============================================================

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# ============================================================
# GLOBAL VARIABLES
# ============================================================

current_unit = "celsius"

weather_data = None

icon_cache = {}


# ============================================================
# WEATHER CODE MAPPING
# ============================================================

def get_weather_description(code):

    weather_codes = {
        0: "Clear Sky",

        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing Rime Fog",

        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",

        56: "Light Freezing Drizzle",
        57: "Dense Freezing Drizzle",

        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",

        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",

        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",

        77: "Snow Grains",

        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",

        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",

        95: "Thunderstorm",

        96: "Thunderstorm With Slight Hail",
        99: "Thunderstorm With Heavy Hail"
    }

    return weather_codes.get(
        code,
        "Unknown Weather"
    )


# ============================================================
# WEATHER EMOJI
# ============================================================

def get_weather_emoji(code):

    if code == 0:
        return "☀️"

    elif code in [1, 2]:
        return "🌤️"

    elif code == 3:
        return "☁️"

    elif code in [45, 48]:
        return "🌫️"

    elif code in [51, 53, 55, 56, 57]:
        return "🌦️"

    elif code in [61, 63, 65, 66, 67]:
        return "🌧️"

    elif code in [71, 73, 75, 77, 85, 86]:
        return "❄️"

    elif code in [80, 81, 82]:
        return "🌦️"

    elif code in [95, 96, 99]:
        return "⛈️"

    return "🌤️"


# ============================================================
# SHOW ERROR
# ============================================================

def show_error(message):

    error_label.config(
        text=message
    )


# ============================================================
# CLEAR ERROR
# ============================================================

def clear_error():

    error_label.config(
        text=""
    )


# ============================================================
# FORMAT TEMPERATURE
# ============================================================

def format_temperature(temp):

    if current_unit == "celsius":

        return f"{temp:.1f} °C"

    else:

        fahrenheit = (
            temp * 9 / 5
        ) + 32

        return f"{fahrenheit:.1f} °F"


# ============================================================
# GET CITY COORDINATES
# ============================================================

def get_city_coordinates(city):

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data:

        return None

    if len(data["results"]) == 0:

        return None

    result = data["results"][0]

    return {
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "name": result["name"],
        "country": result.get(
            "country",
            ""
        ),
        "admin1": result.get(
            "admin1",
            ""
        )
    }


# ============================================================
# GET WEATHER DATA
# ============================================================

def get_weather():

    global weather_data

    city = city_entry.get().strip()

    clear_error()

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not city:

        show_error(
            "Please enter a city name."
        )

        return

    # --------------------------------------------------------
    # Find coordinates
    # --------------------------------------------------------

    try:

        location = get_city_coordinates(
            city
        )

        if location is None:

            show_error(
                f"City '{city}' was not found."
            )

            return

        latitude = location["latitude"]

        longitude = location["longitude"]

        # ----------------------------------------------------
        # Weather API parameters
        # ----------------------------------------------------

        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "weather_code,"
                "wind_speed_10m"
            ),

            "hourly": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "weather_code,"
                "wind_speed_10m,"
                "precipitation_probability"
            ),

            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "weather_code,"
                "precipitation_probability_max,"
                "sunrise,"
                "sunset"
            ),

            "temperature_unit": "celsius",

            "wind_speed_unit": "kmh",

            "timezone": "auto",

            "forecast_days": 5
        }

        response = requests.get(
            WEATHER_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        weather_data = response.json()

        # ----------------------------------------------------
        # Display everything
        # ----------------------------------------------------

        display_current_weather(
            location
        )

        display_hourly_forecast()

        display_daily_forecast()

    except requests.exceptions.Timeout:

        show_error(
            "Request timed out. Please check your internet connection."
        )

    except requests.exceptions.ConnectionError:

        show_error(
            "Network error. Please check your internet connection."
        )

    except requests.exceptions.RequestException:

        show_error(
            "Unable to connect to the weather service."
        )

    except Exception as e:

        show_error(
            f"Something went wrong: {str(e)}"
        )


# ============================================================
# CURRENT WEATHER
# ============================================================

def display_current_weather(location):

    current = weather_data["current"]

    temperature = current[
        "temperature_2m"
    ]

    feels_like = current[
        "apparent_temperature"
    ]

    humidity = current[
        "relative_humidity_2m"
    ]

    wind_speed = current[
        "wind_speed_10m"
    ]

    weather_code = current[
        "weather_code"
    ]

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location_text = location["name"]

    if location["admin1"]:

        location_text += (
            f", {location['admin1']}"
        )

    if location["country"]:

        location_text += (
            f", {location['country']}"
        )

    city_label.config(
        text=location_text
    )

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    temperature_label.config(
        text=format_temperature(
            temperature
        )
    )

    feels_label.config(
        text=(
            "Feels like: "
            + format_temperature(
                feels_like
            )
        )
    )

    # --------------------------------------------------------
    # Weather condition
    # --------------------------------------------------------

    condition_label.config(
        text=(
            get_weather_emoji(weather_code)
            + " "
            + get_weather_description(
                weather_code
            )
        )
    )

    # --------------------------------------------------------
    # Humidity
    # --------------------------------------------------------

    humidity_label.config(
        text=f"Humidity: {humidity}%"
    )

    # --------------------------------------------------------
    # Wind
    # --------------------------------------------------------

    wind_label.config(
        text=f"Wind Speed: {wind_speed} km/h"
    )


# ============================================================
# HOURLY FORECAST
# ============================================================

def display_hourly_forecast():

    # Remove old widgets

    for widget in hourly_frame.winfo_children():

        widget.destroy()

    hourly = weather_data["hourly"]

    times = hourly["time"]

    temperatures = hourly[
        "temperature_2m"
    ]

    codes = hourly[
        "weather_code"
    ]

    humidity = hourly[
        "relative_humidity_2m"
    ]

    precipitation = hourly[
        "precipitation_probability"
    ]

    # --------------------------------------------------------
    # Show next 6 hours
    # --------------------------------------------------------

    for i in range(6):

        card = tk.Frame(
            hourly_frame,
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=8
        )

        card.pack(
            side="left",
            padx=4
        )

        # Time

        time_text = times[i]

        time_text = time_text[
            11:16
        ]

        tk.Label(
            card,
            text=time_text,
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack()

        # Emoji

        tk.Label(
            card,
            text=get_weather_emoji(
                codes[i]
            ),
            font=("Arial", 24)
        ).pack()

        # Temperature

        tk.Label(
            card,
            text=format_temperature(
                temperatures[i]
            ),
            font=(
                "Arial",
                11,
                "bold"
            )
        ).pack()

        # Humidity

        tk.Label(
            card,
            text=f"Humidity: {humidity[i]}%"
        ).pack()

        # Rain probability

        tk.Label(
            card,
            text=f"Rain: {precipitation[i]}%"
        ).pack()


# ============================================================
# DAILY FORECAST
# ============================================================

def display_daily_forecast():

    for widget in daily_frame.winfo_children():

        widget.destroy()

    daily = weather_data["daily"]

    dates = daily["time"]

    max_temps = daily[
        "temperature_2m_max"
    ]

    min_temps = daily[
        "temperature_2m_min"
    ]

    codes = daily[
        "weather_code"
    ]

    rain_probability = daily[
        "precipitation_probability_max"
    ]

    # --------------------------------------------------------
    # Display 5 days
    # --------------------------------------------------------

    for i in range(5):

        card = tk.Frame(
            daily_frame,
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=10
        )

        card.pack(
            side="left",
            padx=5
        )

        # Date

        tk.Label(
            card,
            text=dates[i],
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack()

        # Weather emoji

        tk.Label(
            card,
            text=get_weather_emoji(
                codes[i]
            ),
            font=("Arial", 25)
        ).pack()

        # Condition

        tk.Label(
            card,
            text=get_weather_description(
                codes[i]
            ),
            wraplength=100
        ).pack()

        # Maximum

        tk.Label(
            card,
            text=(
                "Max: "
                + format_temperature(
                    max_temps[i]
                )
            ),
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack()

        # Minimum

        tk.Label(
            card,
            text=(
                "Min: "
                + format_temperature(
                    min_temps[i]
                )
            )
        ).pack()

        # Rain

        tk.Label(
            card,
            text=(
                f"Rain: "
                f"{rain_probability[i]}%"
            )
        ).pack()


# ============================================================
# TOGGLE CELSIUS / FAHRENHEIT
# ============================================================

def toggle_unit():

    global current_unit

    if current_unit == "celsius":

        current_unit = "fahrenheit"

        unit_button.config(
            text="Switch to °C"
        )

    else:

        current_unit = "celsius"

        unit_button.config(
            text="Switch to °F"
        )

    # Refresh displayed values

    if weather_data is not None:

        # Current weather

        current = weather_data["current"]

        temperature_label.config(
            text=format_temperature(
                current[
                    "temperature_2m"
                ]
            )
        )

        feels_label.config(
            text=(
                "Feels like: "
                + format_temperature(
                    current[
                        "apparent_temperature"
                    ]
                )
            )
        )

        display_hourly_forecast()

        display_daily_forecast()


# ============================================================
# SEARCH WHEN ENTER IS PRESSED
# ============================================================

def search_on_enter(event):

    get_weather()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "🌤️ Weather App - Open-Meteo"
)

root.geometry(
    "1150x850"
)

root.resizable(
    False,
    False
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="🌤️ Weather App",
    font=(
        "Arial",
        26,
        "bold"
    )
)

title_label.pack(
    pady=15
)


subtitle_label = tk.Label(
    root,
    text=(
        "Real-time weather powered by Open-Meteo"
    ),
    font=(
        "Arial",
        11
    )
)

subtitle_label.pack()


# ============================================================
# SEARCH FRAME
# ============================================================

search_frame = tk.Frame(
    root
)

search_frame.pack(
    pady=20
)


city_entry = tk.Entry(
    search_frame,
    width=30,
    font=(
        "Arial",
        13
    )
)

city_entry.grid(
    row=0,
    column=0,
    padx=5
)

city_entry.insert(
    0,
    "Lucknow"
)


get_weather_button = tk.Button(
    search_frame,
    text="Get Weather",
    command=get_weather,
    font=(
        "Arial",
        11,
        "bold"
    ),
    width=15
)

get_weather_button.grid(
    row=0,
    column=1,
    padx=5
)


unit_button = tk.Button(
    search_frame,
    text="Switch to °F",
    command=toggle_unit,
    font=(
        "Arial",
        11
    ),
    width=15
)

unit_button.grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# ERROR LABEL
# ============================================================

error_label = tk.Label(
    root,
    text="",
    font=(
        "Arial",
        11
    )
)

error_label.pack(
    pady=5
)


# ============================================================
# CURRENT WEATHER
# ============================================================

current_frame = tk.LabelFrame(
    root,
    text="Current Weather",
    font=(
        "Arial",
        13,
        "bold"
    ),
    padx=20,
    pady=15
)

current_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


city_label = tk.Label(
    current_frame,
    text="Search for a city",
    font=(
        "Arial",
        20,
        "bold"
    )
)

city_label.pack()


temperature_label = tk.Label(
    current_frame,
    text="-- °C",
    font=(
        "Arial",
        30,
        "bold"
    )
)

temperature_label.pack(
    pady=5
)


feels_label = tk.Label(
    current_frame,
    text="Feels like: --"
)

feels_label.pack()


condition_label = tk.Label(
    current_frame,
    text="Condition",
    font=(
        "Arial",
        14
    )
)

condition_label.pack(
    pady=5
)


humidity_label = tk.Label(
    current_frame,
    text="Humidity: --"
)

humidity_label.pack()


wind_label = tk.Label(
    current_frame,
    text="Wind Speed: --"
)

wind_label.pack()


# ============================================================
# HOURLY FORECAST
# ============================================================

hourly_title = tk.Label(
    root,
    text="⏰ Next 6 Hours",
    font=(
        "Arial",
        15,
        "bold"
    )
)

hourly_title.pack(
    pady=10
)


hourly_frame = tk.Frame(
    root
)

hourly_frame.pack()


# ============================================================
# DAILY FORECAST
# ============================================================

daily_title = tk.Label(
    root,
    text="📅 5-Day Forecast",
    font=(
        "Arial",
        15,
        "bold"
    )
)

daily_title.pack(
    pady=15
)


daily_frame = tk.Frame(
    root
)

daily_frame.pack()


# ============================================================
# ENTER KEY
# ============================================================

city_entry.bind(
    "<Return>",
    search_on_enter
)


# ============================================================
# START APP
# ============================================================

root.mainloop()