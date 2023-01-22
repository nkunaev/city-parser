import os.path
import json
import csv

WORKDIR = 'output'


def save_in_json(name, data: dict):
    with open(os.path.join(WORKDIR, name + '.json'), 'a') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print('Done!')


def save_in_csv(name, data: dict):
    with open(os.path.join(WORKDIR, name + '.csv'), 'a', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(data[0].keys())

    for string in data:
        with open(os.path.join(WORKDIR, name + '.csv'), 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            print(string)
            writer.writerow(string.values())
    print('Done!')


def save_file(data: dict, name: str):
    num = int(input('''Сбор информации завершен! В каком формате сохранить файл? "\n"
    1 - в json, 2 - в csv "\n" >>> '''))
    if num == 1:
        save_in_json(name, data)
    elif num == 2:
        save_in_csv(name, data)
    else:
        raise 'Не выбрано как сохранить результат'
