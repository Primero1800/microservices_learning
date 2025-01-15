import urllib.parse

import requests

def get_response_from_localhost():
    url = 'http://127.0.0.1:8000/'
    responce = requests.get(url)
    return responce.content.decode('utf-8')


def image_loader(url, file_name=None):
    # image = requests.get('https://primero1800.store/media/images/104/1.png')
    image = requests.get(url)
    if not file_name:
        file_name = urllib.parse.urlsplit(url).path.split('/')[-1]
        if file_name:
            with open(file_name, 'wb') as file:
                file.write(image.content)


if __name__ == "__main__":

    # image_loader('https://primero1800.store/media/images/104/1.png')
    # get_response_from_localhost()
    pass





