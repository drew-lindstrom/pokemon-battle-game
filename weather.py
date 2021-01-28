from pokemon import Pokemon

current_weather = "Clear Skies"
weather_counter = None


def set_weather(weather, counter):
    global current_weather
    global weather_counter
    current_weather = weather
    weather_counter = counter