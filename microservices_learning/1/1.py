import aiohttp
import asyncio
import asyncpg

DB_ENGINE='django.db.backends.postgresql'
DB_HOST='localhost'
DB_PORT=5432
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_NAME='mineshop7'

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        "https://primero1800.store/api",
        "https://primero1800.store/api/detail/2/",
        "https://primero1800.store/api/admin/orders/",
    ]
    async with aiohttp.ClientSession() as session:
        in_processing = [asyncio.create_task(fetch_data(session, url)) for url in urls]
        while in_processing:
            ready, in_processing = await asyncio.wait(in_processing, return_when=asyncio.FIRST_COMPLETED)
            for task in ready:
                print(task.result())
                print('**************')


async def fetch_users_backfeedsfrom_db():
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD,
                                 database=DB_NAME, host=DB_HOST)

    users = await conn.fetch('SELECT id, email FROM users_user')
    data = {}

    for user in users:
        data[user['email']] = {
            'id': user['id'],
            'posts': [dict(item) for item in await conn.fetch(f"SELECT name, review, title FROM posts_post LEFT JOIN store_product ON posts_post.product_id = store_product.id WHERE user_id = {user['id']}")],
           'votes': [dict(item) for item in await conn.fetch(f"SELECT name, review, stars, title FROM store_vote LEFT JOIN store_product ON store_vote.product_id = store_product.id WHERE user_id = {user['id']}")]
        }


    await conn.close()
    return data

async def main2():
    user_data = await fetch_users_backfeedsfrom_db()


    for key, dictionary in user_data.items():
        print(f"USER = {key}, ID = {dictionary['id']}")

        if 'posts' in dictionary and dictionary['posts']:
            print('POSTS:')
            for post in dictionary['posts']:
                for key, val in post.items():
                    if val:
                        print(f"    {key.upper()} = {val}")
                print('    -----------------')

        if 'votes' in dictionary and dictionary['votes']:
            print('VOTES:')
            for vote in dictionary['votes']:
                for key, val in vote.items():
                    if val:
                        print(f"    {key.upper()} = {val}")
                print('    -----------------')

        print()


if __name__ == "__main__":
    asyncio.run(main2())