import os
import asyncio
from pathlib import Path
from aiohttp import web
import asyncpg


async def handle(request):
    response = web.StreamResponse()
    response.content_type = "text/plain"
    await response.prepare(request)
    async with request.app["pool"].acquire() as con:
        async with con.transaction():
            async for record in con.cursor("SELECT id,name,num from rows"):
                text = ",".join(map(str, record)) + "\n"
                await response.write(text.encode())

    return response


async def init_app():
    app = web.Application()
    pool = await asyncpg.create_pool(
        database="postgres",
        user="postgres",
        password="password",
        host=os.environ.get("DB_HOST", "localhost"),
    )
    statement = """
    insert into rows(name, num) values ($1, $2);
    """
    values = [[f"Row {i}", i] for i in range(10)]
    async with pool.acquire() as con:
        await con.executemany(statement, values)

    app["pool"] = pool

    app.router.add_route("GET", "/", handle)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=os.environ.get("PORT", 8081))
