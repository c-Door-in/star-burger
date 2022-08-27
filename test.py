import requests

from geopy import distance

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def main():
    apikey = '92039794-2636-445f-9d80-6f0eea0b2da7'
    lon1, lat1 = fetch_coordinates(apikey, 'Фролково, Егорьевский район')
    lon2, lat2 = fetch_coordinates(apikey, 'Саратов')
    print(distance.distance((lat1, lon1), ((lat2, lon2))).km)


if __name__ == '__main__':
    main()