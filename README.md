# wttr-cli

wttr-cli is a CLI app to check the weather outside, its feature include:
current weather, 3 days weather forecast with 3 hours intervals and user's
preferred language. This project is a part of My learning journey to make
something with code and to understanding how to use API, retrieve a data from
API, processing the data and how to make it presentable to a user

## Usage

- Check current weather  

```sh
python wttr-cli [CITY]
```

![Image of current weather](https://github.com/Lmanangka/wttr-cli/blob/main/img/current_weather.png?raw=true)

- Check weather forecast  

```sh
python wttr-cli [CITY] [-f]
```
or  
```sh
python wttr-cli [CITY] [--forecast]
```

![Image of weather forecast](https://github.com/Lmanangka/wttr-cli/blob/main/img/weather_forecast.png?raw=true)

- To change a language

```sh
python wttr-cli [CITY] [-l] [LANGUAGE]
```
or
```sh
python wttr-cli [CITY] [--lang] [LANGUAGE]
```

![Image of current weather with chosen language](https://github.com/Lmanangka/wttr-cli/blob/main/img/current_weather_with_chosen_language.png?raw=true)

[Supported language](https://openweathermap.org/current#multi)

- Show help text

```sh
python wttr-cli [-h]
```

![Image of wttr-cli help text](https://github.com/Lmanangka/wttr-cli/blob/main/img/help_text.png?raw=true)

## References and Credits
- [openweathermap](https://openweathermap.org/) for providing data for free
- [Build Command-line Interfaces with argparse](https://realpython.com/command-line-interfaces-python-argparse/)
- [Make a good CLI interface and using API](https://realpython.com/build-a-python-weather-app-cli/)
