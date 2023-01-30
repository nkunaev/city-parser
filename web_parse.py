import requests
import sys
from bs4 import BeautifulSoup
from sql_connector import check_city
from sql_connector import update_cities_in_list
from sql_connector import select_city_from_list
from sql_connector import update_houses_info

main_page_url = "https://dom.mingkh.ru"
header = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
}


def get_city(city: str) -> str:
    if city.strip() == '':
        exit("Нужно написать название города")
    city = city.lower()
    if check_city(city) == 1:
        print("Такого города нет в базе, можете попробовать ее обновить и попробовать снова. ")
    elif city == 'search':
        select_city_from_list('get_cities')
        sys.exit(0)
    need_update = int(input("Нужно ли обновить список городов? '\n' >>> Да - нажми 1 '\t' >>> Нет - нажми 0 '\n' >>> "))
    if need_update == 1:
        regions = requests.get('https://dom.mingkh.ru/moskovskaya-oblast/#all_cities', headers=header)
        soup = BeautifulSoup(regions.text, "lxml")
        data = soup.find_all("ul", class_="list-unstyled list-columns")
        for data_city in data[0].find_all("li"):
            url = "https://dom.mingkh.ru" + data_city.find("a").get("href") + 'houses?page='
            name = data_city.find("a").text.replace("\n", "").lower()
            update_cities_in_list(name, url)
        for data_city in data[1].find_all("li"):
            url = "https://dom.mingkh.ru" + data_city.find("a").get("href") + 'houses?page='
            name = data_city.find("a").text.replace("\n", "").lower()
            update_cities_in_list(name, url)
    if check_city(city) == 0:
        return select_city_from_list('get_url', city)
    else:
        print("Такого города нет в списке населенных пунктов. ")
        sys.exit(0)


def max_page(city):
    url = f"{get_city(city)} + '1'"
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    pages_list = [1]
    # Значение = 1, тк в некоторых городах только 1 страница с улицами, тогда тег 'pagination' отсутствует
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


def parse_result(city: str):
    print("Получили данные, начинаем записывать результат...")
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
        location = soup.find("div", class_='block-heading-two').text.removeprefix(' Анкета дома «').removesuffix(
            '» ')
        update_houses_info(location,
                           union_vals.get('Тип дома', "Нет данных"),
                           union_vals.get('Жилых помещений', "Нет данных"),
                           union_vals.get('Серия, тип постройки', 1),
                           union_vals.get('Тип перекрытий', "Нет данных"),
                           union_vals.get('Материал несущих стен', "Нет данных"),
                           union_vals.get('Тип мусоропровода', "Нет данных"),
                           union_vals.get('Дом признан аварийным', "Нет данных"),
                           union_vals.get('Детская площадка', "Нет данных"),
                           union_vals.get('Спортивная площадка', "Нет данных"),
                           union_vals.get('Кадастровый номер', "Нет данных")
                           )
