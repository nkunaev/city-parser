from save_method import save_file
from web_parse import parse_result
from test import test_parce


print('''   Это скрипт для парсинга сайта https://dom.mingkh.ru/ по городам Московской области.
Название интересующего города нужно вводить на русском языке. Для получения списка городов 
введите "search".
    Файл с результатом работы будет записан в директорию скрипта в формате название_города.json ''')
print()
city_name = input("Введите название города: ").lower()
data = parse_result(city_name)
# city_name = "test"
# data = test_parce()
save_file(data, city_name)

