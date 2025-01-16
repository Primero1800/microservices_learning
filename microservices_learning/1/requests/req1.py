import urllib.parse

import requests


def get_response_from_localhost(params=None):
    url = 'http://127.0.0.1:8000/'
    responce = requests.get(url, params=params)
    return responce.content.decode('utf-8')


def image_loader(url, file_name=None):
    # image = requests.get('https://primero1800.store/media/images/104/1.png')
    image = requests.get(url)
    if not file_name:
        file_name = urllib.parse.urlsplit(url).path.split('/')[-1]
        if file_name:
            with open(file_name, 'wb') as file:
                file.write(image.content)


def get_weather(city):
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = { 'key': '1c82927a15dd4ea78d2130958251501',
               'q': city,
               'format': 'json',
               'num_of_days': 256,
               'lang': 'ru'}
    r = requests.get(url, params=params)
    the_weather = r.json()
    if 'data' in the_weather:
        if 'current_condition' in the_weather['data']:
            try:
                return the_weather['data']['current_condition'][0]
            except(IndexError, TypeError):
                return 'Server Error'
    return 'Server Error'


if __name__ == "__main__":

    cities = ['Minsk', 'Moscow', 'Казань',]
    params = {'key': '1c82927a15dd4ea78d2130958251501',
              'q': cities[0],
              'format': 'json',
              'num_of_days': 256,
              'lang': 'ru'}

    # image_loader('https://primero1800.store/media/images/104/1.png')
    print(get_response_from_localhost(params))

    # for city in cities:
    #     weather = get_weather(city)
    #     print(f'{city}: Погода сейчас {weather["temp_C"]}, ощущается как {weather["FeelsLikeC"]}')





