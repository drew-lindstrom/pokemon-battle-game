from pokemon import Pokemon


class Weather:
    def __init__(self):
        self.current_weather = "Clear Skies"
        self.weather_counter = None

    def set_weather(self, weather, counter):
        self.current_weather = weather
        self.weather_counter = counter

    def clear_weather(self):
        if self.weather_counter == 0:
            self.current_weather = "Clear Skies"
