import requests
import sys
from bs4 import BeautifulSoup

main_page_url = "https://dom.mingkh.ru"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}


def test_parce():
    city_name = "vysokovsk"
    my_dict = {city_name: []}
    url = "https://dom.mingkh.ru/moskovskaya-oblast/vysokovsk/1154605"
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
    pre_dict = {
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
    }
    my_dict[city_name].append(pre_dict)
    return my_dict
