import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Unit Conversion Functions
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def kmh_to_mps(kmh):
    return kmh / 3.6

def kmh_to_mph(kmh):
    return kmh / 1.609

def mps_to_kmh(mps):
    return mps * 3.6

def mps_to_mph(mps):
    return mps * 2.237

# Function to get coordinates using Nominatim API
def get_coordinates(place_name):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json&limit=1"
        headers = {"User-Agent": "WeatherApp/1.0 (your_email@example.com)"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]
                return latitude, longitude
            else:
                return None, None
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

# Function to fetch weather data using Open-Meteo API
def get_weather(latitude, longitude):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url, timeout=10)
        data = response.json()

        if "current_weather" in data:
            temperature_celsius = data['current_weather']['temperature']
            wind_speed_kmh = data['current_weather']['windspeed']
            weather_code = data['current_weather']['weathercode']

            weather_descriptions = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 61: "Rain showers",
                80: "Rain with thunderstorm",
            }
            weather_description = weather_descriptions.get(weather_code, "Unknown condition")

            return temperature_celsius, wind_speed_kmh, weather_description
        else:
            return None, None, "Unable to fetch weather data"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None, "Error fetching weather data"

# Function to update weather information on the GUI
def update_weather():
    place_name = entry_place.get()
    if not place_name:
        messagebox.showerror("Input Error", "Please enter a place name!")
        return

    lat, lon = get_coordinates(place_name)
    if lat and lon:
        temperature_celsius, wind_speed_kmh, weather_description = get_weather(lat, lon)
        if temperature_celsius is not None:
            # Get the selected units
            temp_unit = temp_unit_var.get()
            wind_speed_unit = wind_speed_unit_var.get()

            # Convert temperature to selected unit
            if temp_unit == "Fahrenheit":
                temperature = celsius_to_fahrenheit(temperature_celsius)
            elif temp_unit == "Kelvin":
                temperature = celsius_to_kelvin(temperature_celsius)
            else:
                temperature = temperature_celsius

            # Convert wind speed to selected unit
            if wind_speed_unit == "m/s":
                wind_speed = kmh_to_mps(wind_speed_kmh)
            elif wind_speed_unit == "mph":
                wind_speed = kmh_to_mph(wind_speed_kmh)
            else:
                wind_speed = wind_speed_kmh

            # Update labels with the converted values
            label_temperature.config(text=f"Temperature: {temperature:.2f} {temp_unit}")
            label_wind_speed.config(text=f"Wind Speed: {wind_speed:.2f} {wind_speed_unit}")
            label_weather_description.config(text=f"Condition: {weather_description}")
            update_weather_icon(weather_description)
        else:
            label_temperature.config(text="Error fetching data.")
            label_wind_speed.config(text="")
            label_weather_description.config(text="")
    else:
        messagebox.showerror("Location Error", "Could not find the location. Please try again.")

# Function to update weather icon based on the weather description
def update_weather_icon(weather_description):
    icon_mapping = {
        "Clear sky": "clear_sky.png",
        "Mainly clear": "clear_sky.png",
        "Partly cloudy": "cloudy.png",
        "Overcast": "overcast.png",
        "Fog": "fog.png",
        "Depositing rime fog": "fog.png",
        "Light drizzle": "drizzle.png",
        "Rain showers": "rain.png",
        "Rain with thunderstorm": "thunderstorm.png",
    }

    icon_file = icon_mapping.get(weather_description, "default.png")

    try:
        img = Image.open(icon_file)
        img = img.resize((50, 50), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label_icon.config(image=img)
        label_icon.image = img
    except FileNotFoundError:
        label_icon.config(text="No icon available")

# GUI Setup using Tkinter
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")

# Labels for displaying weather data
label_title = tk.Label(root, text="Weather App", font=("Helvetica", 16))
label_title.pack(pady=10)

entry_place = tk.Entry(root, font=("Helvetica", 14))
entry_place.pack(pady=10)

button_fetch_weather = tk.Button(root, text="Get Weather", font=("Helvetica", 14), command=update_weather)
button_fetch_weather.pack(pady=10)

label_temperature = tk.Label(root, text="Temperature: --°C", font=("Helvetica", 12))
label_temperature.pack(pady=5)

label_wind_speed = tk.Label(root, text="Wind Speed: -- km/h", font=("Helvetica", 12))
label_wind_speed.pack(pady=5)

label_weather_description = tk.Label(root, text="Condition: --", font=("Helvetica", 12))
label_weather_description.pack(pady=5)

label_icon = tk.Label(root)
label_icon.pack(pady=10)

# Dropdown menu for temperature units
temp_unit_var = tk.StringVar(value="Celsius")
temp_unit_menu = tk.OptionMenu(root, temp_unit_var, "Celsius", "Fahrenheit", "Kelvin")
temp_unit_menu.pack(pady=5)

# Dropdown menu for wind speed units
wind_speed_unit_var = tk.StringVar(value="km/h")
wind_speed_unit_menu = tk.OptionMenu(root, wind_speed_unit_var, "km/h", "m/s", "mph")
wind_speed_unit_menu.pack(pady=5)

# Run the GUI application
root.mainloop()
