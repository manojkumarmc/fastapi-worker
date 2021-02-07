import asyncio
from typing import Optional, TypedDict
from fastapi import FastAPI, BackgroundTasks
from loguru import logger
from secrets import token_hex
from random import randint
from datetime import datetime
from pprint import pprint as pp


class TM(TypedDict):
    key: float


tm: TM = {"key": 0.0}


async def add_worker_info(key: str, val: float):
    global tm
    tm[key] = val


async def worker(name: Optional[str] = None):
    global tm
    interval: float = randint(1, 10) / 10
    print(f"The interval of {name} is {interval}")
    await add_worker_info(name, interval)
    pp(tm)
    while True:
        # logger.info(f"Worker in progress {name}")
        await asyncio.sleep(interval)


def init():
    loop = asyncio.get_running_loop()
    print(id(loop))
    for x in range(3):
        loop.create_task(worker(token_hex(10)))


app = FastAPI(on_startup=[init])


@app.get("/")
async def first_method():
    return {f"Hello World at {datetime.now()}"}


# this works
@app.get("/start")
async def starter(bt: BackgroundTasks):
    bt.add_task(worker)
