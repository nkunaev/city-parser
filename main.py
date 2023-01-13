import requests, re

def searchCity():
    city_ru = 'Дубна'
    r = requests.get('https://dom.mingkh.ru/moskovskaya-oblast/#all_cities')
    var = re.findall(f'<a href="(/moskovskaya-oblast/.{1,15})">{city_ru}</a>', r.text)
    print(var)
    for i in var:
       print(i.strip().replace(' ', ''))


searchCity()+