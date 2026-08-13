def celsius_to_fahrenheit(celsius):

    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):

    return (fahrenheit - 32) * 5 / 9


def parse_weather_data(data):

    return {
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "wind_speed": data["wind_speed"],
        "description": data["description"]
    }


def test_celsius_to_fahrenheit():

    assert celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_100():

    assert celsius_to_fahrenheit(100) == 212


def test_fahrenheit_to_celsius():

    assert fahrenheit_to_celsius(32) == 0


def test_weather_data_parsing():

    data = {
        "temperature": 30,
        "humidity": 65,
        "wind_speed": 12,
        "description": "Clear sky"
    }

    result = parse_weather_data(data)

    assert result["temperature"] == 30
    assert result["humidity"] == 65
    assert result["wind_speed"] == 12
    assert result["description"] == "Clear sky"


def test_empty_city():

    city = ""

    assert city.strip() == ""


def test_city_validation():

    city = "Lucknow"

    assert city.strip() != ""