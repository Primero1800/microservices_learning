import requests

def get_responce_from_localhost():
    url = 'http://127.0.0.1:8000/'
    responce = requests.get(url)
    return responce.content.decode('utf-8')

if __name__ == "__main__":

    # image = requests.get('https://primero1800.store/media/images/104/1.png')
    # with open('image1.png', 'wb') as file:
    #     file.write(image.content)

    print(get_responce_from_localhost())


