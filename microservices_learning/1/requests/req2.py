import requests


if __name__ == "__main__":

    query = {'q': 'Hayley Gardner', 'order': 'popular', 'min_width': '100', 'min_height': '80'}
    req = requests.get('<a href="https://pixabay.com/en/photos/">https://pixabay.com/en/photos/</a>', params=query)
    print(req.url)