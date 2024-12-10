from fastapi import FastAPI
import aiomysql

DB_ENGINE='django.db.backends.postgresql'
DB_HOST='localhost'
DB_PORT=5432
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_NAME='mineshop'

app = FastAPI()

pool = None


async def create_pool():
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )
    return pool


async def save_task_to_db(task):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO tasks (task_name) VALUES (%s)", (task,))

@app.on_event("startup")
async def startup_db():
    global pool
    pool = await create_pool()

@app.on_event("shutdown")
async def shutdown_db():
    global pool
    pool.close()
    await pool.wait_closed()

tasks = []

@app.post('/tasks/')
async  def create_task(task: str):
    tasks.append(task)
    return {"message": "Task created successfully"}

@app.get('/tasks/')
async def get_tasks():
    return {'tasks': tasks}
