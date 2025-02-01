import json

import httpx
import uuid



#CAT_URL = "https://cataas.com/cat"
CAT_URL = "https://thecatapi.com/api/images/get?format=src&type=gif"

# DOG_JSON_URL = 'https://api.giphy.com/v1/gifs/search?api_key=EcEFiAw4smzAHJyJLiRunkuguJOwe6wT&q=dog&limit=1'
DOG_JSON_URL = "https://thedogapi.com/api/images/get?format=src&type=gif"


def get_periodictask_name(task):
    result = ''
    headers = task.request.headers
    if headers:
        print(f"**********!!!!!!!!!!!!!!****************** {headers}, items: {headers.items()}")
        result = headers.get('name', '')
    else:
        print("No headers available.")
    return result


def write_result(response, periodictask_name):
    print(f"Inner result Response={response}")
    try:
        if response and response.status_code == 200:
            file_ext = response.headers.get("Content-Type").split('/')[1]
        else:
            file_ext = '.err'
        file_name = str(uuid.uuid4()) + '.' + file_ext

        with open(file_name, 'wb') as file:
            if response and response.status_code == 200:
                for chunk in response.iter_bytes(chunk_size=256):
                    file.write(chunk)
            elif response:
                file.write(f"{response.status_code} -- {response.headers} -- {response.content}".encode())
            else:
                file.write('No response error'.encode())
    except Exception as exc:
        print(response.status_code, periodictask_name, 'Error while writing file')
        return False
    return file_name


def import_url_of_dog(*args, **kwargs):
    search_term = 'dog',
    apikey = 'AIzaSyA9FTUB1l-VzHOCkkwW_mcVi3cYwOCX6YU'
    lmt = 1

    with httpx.Client() as client:
        response = client.get(
            DOG_JSON_URL,
            follow_redirects=True
        )

    d = 2
    if response.status_code == 200:
        return json.loads(response.content)

    return None


if __name__ == "__main__":

    import_url_of_dog()
