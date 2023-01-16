import requests
import sys
from bs4 import BeautifulSoup
from typing import List, Dict, Union

main_page_url = "https://dom.mingkh.ru"
header = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
}


def get_city(city: str) -> List[str]:
    if city.strip():
        exit("Нужно написать название города")

    city = city.lower()
    city_list = {}
    regions = requests.get('https://dom.mingkh.ru/moskovskaya-oblast/#all_cities', headers=header)
    soup = BeautifulSoup(regions.text, "lxml")
    data = soup.find("ul", class_="list-unstyled list-columns")
    for data_city in data.find_all("li"):
        url = "https://dom.mingkh.ru" + data_city.find("a").get("href") + 'houses?page='
        name = data_city.find("a").text.replace("\n", "").lower()
        city_list[name] = url
    if city == "search":
        print("Вот список населенных пунктов:")
        for city_ in city_list.keys():
            print(city_.capitalize())
        sys.exit(0)
    elif city in city_list.keys():
        return city_list[city]
    else:
        print("Такого города нет, вот список населенных пунктов:")
        for city_ in city_list.keys():
            print(city_.capitalize())
        exit()


def max_page(city):
    url = f"{get_city(city)} + '1'"
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    try:  # В маленьких городах только 1 страница с домами, е если pages не отрабатывает, значит страница всего одна
        pages = soup.find("ul", class_="pagination").find_all("li")
        pages_list = []
        """в служебном теге pagination где отображаеся стр. 1-3, след. и последняя, получаем номер последней страницы"""
        for page in pages:
            digit = page.find("a").get("data-ci-pagination-page")
            try:  # Возвращает в ответе и NonType и Empty и цифры, отсеиваем лишнее.
                pages_list.append(int(digit))
            except:
                pass
        max_page = max(pages_list)
        return int(max_page)
    except:
        pass
    return 1


"""парсим страницы по очереди"""


def get_url(city):
    max_page_ = max_page(city)
    print(f"Выбран город {city.capitalize()}, начинаем сбор информации о домах...")
    for num_page in range(1, max_page_ + 1):
        url = f"{get_city(city)}{num_page}"
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("table", class_="table table-bordered table-striped table-hover").find("tbody").find_all("tr")
        for city_link in data:
            url = main_page_url + city_link.find_all("td")[2].find("a").get("href")
            yield url


def parse_result(city: str) -> List[Dict[str, Union[str, int, None]]]:
    print("Получили данные, начинаем записывать результат...")
    my_list = []

    for url in get_url(city):
        union_vals, pre_dict, keys, vals = {}, {}, [], []
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("dl", class_="dl-horizontal house")
        dt_all = data.find_all("dt")
        for dt in dt_all:
            keys.append(dt.text)
        dd_all = data.find_all("dd")
        for dd in dd_all:
            vals.append(dd.text)
        union_vals = dict(zip(keys, vals))
        print(union_vals.get('Адрес', 'Нет данных').removesuffix('   На карте'))

        my_list.append({
            'city': union_vals.get('Адрес', 'Нет данных').split(',')[2].replace(' ', ''),
            'street': union_vals.get('Адрес', 'Нет данных').split(',')[0],
            'num_house': union_vals.get('Адрес', 'Нет данных').split(',')[1].replace(' ', ''),
            'house_type': union_vals.get('Тип дома', "Нет данных"),
            'living_quarters': union_vals.get('Жилых помещений', "Нет данных"),
            'series_and_type_of_construction': union_vals.get('Серия, тип постройки', "Нет данных"),
            'type_of_overlap': union_vals.get('Тип перекрытий', "Нет данных"),
            'wall_material': union_vals.get('Материал несущих стен', "Нет данных"),
            'type_of_garbage_chute': union_vals.get('Тип мусоропровода', "Нет данных"),
            'recognized_as_emergency': union_vals.get('Дом признан аварийным', "Нет данных"),
            'playground': union_vals.get('Детская площадка', "Нет данных"),
            'sports_ground': union_vals.get('Спортивная площадка', "Нет данных"),
            'cadastral_number': union_vals.get('Кадастровый номер', "Нет данных")
        })

    return my_list

