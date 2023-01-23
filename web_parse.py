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
    if city.strip() == '':
        exit("Нужно написать название города")

    city = city.lower()
    city_list = {}
    regions = requests.get('https://dom.mingkh.ru/moskovskaya-oblast/#all_cities', headers=header)
    soup = BeautifulSoup(regions.text, "lxml")
    data = soup.find_all("ul", class_="list-unstyled list-columns")
    for data_city in data[0].find_all("li"):
        url = "https://dom.mingkh.ru" + data_city.find("a").get("href") + 'houses?page='
        name = data_city.find("a").text.replace("\n", "").lower()
        city_list[name] = url
    for data_city in data[1].find_all("li"):
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
    pages_list = [
        1]  # Значение = 1, тк в некоторых городах только 1 страница с улицами, тогда тег 'pagination' отсутствует
    if soup.find(class_="pagination"):
        pages = soup.find("ul", class_="pagination").find_all("li")
        for page in pages:
            digit = page.find("a").get("data-ci-pagination-page")
            if digit is None:
                continue
            if digit.isdigit():
                pages_list.append(int(digit))
    return max(pages_list)


def get_url(city):
    max_page_ = max_page(city)
    for num_page in range(1, max_page_ + 1):
        url = f"{get_city(city)}{num_page}"
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("table", class_="table table-bordered table-striped table-hover").find("tbody").find_all("tr")
        for city_link in data:
            url = main_page_url + city_link.find_all("td")[2].find("a").get("href")
            yield url


def get_address(soup) -> dict[str, str]:
    town_keyword = ['дп', 'рп', 'снт', 'дер', 'с']
    street_keyword = ['ул', 'пр-кт', 'пер', 'туп', 'кв-л']
    location_dict = {'city': '',
                     'town': 'Нет данных',
                     'street': 'Нет данных',
                     'house': ''
                     }
    location = soup.find("div", class_='block-heading-two').text.removeprefix(' Анкета дома «').removesuffix(
        '» ').split(',')
    spaces = 0
    for i in location[1].strip():
        if i == ' ':
            spaces += 1
    if len(location) == 3 and spaces > 0:
        location_dict.update({
            'city': location[0].strip(),
            'street': location[1].strip(),
            'house': location[2].strip()
        })
    elif len(location) == 3 and spaces == 0:
        location_dict.update({
            'city': location[0].strip(),
            'town': location[1].strip(),
            'house': location[2].strip()
        })

    elif len(location) == 4:
        location_dict.update({
            'city': location[0].strip(),
            'town': location[1].strip(),
            'street': location[2].strip(),
            'house': location[3].strip()
        })
    return location_dict


def parse_result(city: str) -> List[Dict[str, Union[str, int, None]]]:
    print("Получили данные, начинаем записывать результат...")
    my_list = []
    for url in get_url(city):
        union_vals, keys, vals = {}, [], []
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
        local_address = get_address(soup)
        print(local_address.get('city'), ' ', local_address.get('street'), ' ', local_address.get('house'))
        my_list.append({
            'city': local_address.get('city'),
            'town': local_address.get('town'),
            'street': local_address.get('street'),
            'house': local_address.get('house'),
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
