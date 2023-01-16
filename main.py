from transliterate import translit
import json, csv, os
from web_parse import parse_result


print('''   Это скрипт для парсинга сайта https://dom.mingkh.ru/ по городам Московской области.
Название интересующего города нужно вводить на русском языке. Для получения списка городов 
введите "search".
    Файл с результатом работы будет записан в директорию скрипта в формате название_города.json ''')
print()
city_name_ru = input("Введите название города: ").lower()
city_name = translit(city_name_ru, language_code='ru', reversed=True)
current_path = os.path.dirname(os.path.abspath("main.py"))
if os.name == "nt":
    current_path += '\\' + f"{city_name}"
elif os.name == "posix":
    current_path += '/' + f"{city_name}"
else:
    #print("Не известная операционная система! ")
    #sys.exit(0)

    exit("Не известная операционная система! ")

data = parse_result(city_name_ru)

print("Сбор информации завершен. В каком формате сохранить?")
save_file_type = int(input("json - нажми '1', csv - '2'\n"))
if save_file_type == 1:
    current_path += ".json"
    with open(current_path, 'w') as file:
        json.dump(data, file, indent=2)

elif save_file_type == 2:
    current_path += ".csv"
    data_raw = data[city_name]
    with open(current_path, 'a', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(*data_raw[0].keys())

    for info in data_raw:
        with open(current_path, 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(*info.values())

print("Done!")