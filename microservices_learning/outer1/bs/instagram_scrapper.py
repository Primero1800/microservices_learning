import asyncio

import httpx
from bs4 import BeautifulSoup
from httpx import RequestError, HTTPStatusError

class InstagramClient:
    def __init__(self):
        self.username = None
        self.password = None
        self.client = httpx.AsyncClient()

    def get_username_and_password(self):
        self.username = input('Username: ')
        self.password = input('Password: ')

    async def login(self):
        self.get_username_and_password()
        response = await self.client.get('https://www.instagram.com/accounts/login/')
        csrf_token = response.cookies.get('csrftoken')
        login_data = {
            'username': self.username,
            'password': self.password
        }

        response = await self.client.post(
            #'https://www.instagram.com/accounts/login/ajax/',
            'https://www.instagram.com/',
            data=login_data,
            headers={'X-CSRFToken': csrf_token}
        )
        d = 2
        #if response.status_code == 200 and response.json().get('authenticated'):
        if response.status_code == 200:
            print("Успешно вошли в аккаунт")
        else:
            print("Ошибка при входе")
            return False
        return True

    async def get_user_page(self, user):
        try:
            response = await self.client.get(f'https://www.instagram.com/{user}/')
            response.raise_for_status()
            return response.text
        except (RequestError, HTTPStatusError) as error:
            print(f'Вай-вай-вай. {error} упаль, однако')
            return False

    async def close(self):
        await self.client.aclose()


class SiteParser:
    def __init__(self, html):
        self.html = html

    def parse_site(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        img_list = soup.findAll('img')
        imgs = []
        try:
            for img in img_list:
                if 'data-echo' in img.attrs:
                    imgs.append(img.attrs['data-echo'])
                elif 'src' in img.attrs:
                    imgs.append(img.attrs['src'])
        except (KeyError, AttributeError, TypeError) as error:
            print(f'Raised error: {error} while parsing. Result may be not valid')
        return imgs

async def main():
    client = InstagramClient()
    if await client.login():
        user = input('Enter username for parsing page: ')
        user_page_html = await client.get_user_page(user)
        if user_page_html:
            print('GOT IT!!!!!!!!!')
        else:
            print('OOPS!!!!')

    await client.close()

    parser = SiteParser(user_page_html)
    imgs = parser.parse_site()
    print(*imgs, sep='\n\n\n')


if __name__ == "__main__":
    asyncio.run(main())