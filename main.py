import requests
from bs4 import BeautifulSoup


def get_city(city: str):
    if type(city) != str:
        print("Нужно написать название города" + '\n')
        return 0
    city = city.lower()
    city_list = {}
    regions = requests.get('https://dom.mingkh.ru/moskovskaya-oblast/#all_cities')
    soup = BeautifulSoup(regions.text, "lxml")
    data = soup.find("ul", class_="list-unstyled list-columns")
    for data_city in data.find_all("li"):
        url = "https://dom.mingkh.ru" + data_city.find("a").get("href")
        name = data_city.find("a").text.replace("\n", "").lower()
        city_list[name] = url
    if city == "search":
        print("Вот список населенных пунктов:")
        for city_ in city_list.keys():
            print(city_.capitalize())
    elif city in city_list.keys():
        return city_list[city]
    else:
        print("Такого города нет, вот список населенных пунктов:")
        for city_ in city_list.keys():
            print(city_.capitalize())
        return 0


print(get_city())
