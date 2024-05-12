import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from init import app

if __name__ == "__main__":
    config = Config()
    config.bind = ['0.0.0.0:3000']
    config.application_path = 'main:app'
    asyncio.run(serve(app, config))
