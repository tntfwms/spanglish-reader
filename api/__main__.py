from logging import getLogger
from aiohttp import web
from typing import AsyncIterator
from aiohttp import ClientSession

from .routes import upload_api_page
import config

logger = getLogger('App Factory')

async def client_session_ctx(app: web.Application) -> AsyncIterator:
    logger.debug('Creating ClientSession')
    app['client_session'] = ClientSession()

    yield

    logger.debug('Closing ClientSession')
    await app['client_session'].close()


async def app_factory() -> web.Application:
    logger.debug('Creating Application (entering APP Factory)')
    app = web.Application()

    logger.debug('Adding Routes')
    app.add_routes(
        [
            web.post('/api/v1/upload', upload_api_page),
        ],
    )


    logger.debug('Registering Cleanup contexts')
    app.cleanup_ctx.append(client_session_ctx)

    logger.debug('APP is now prepared and can be returned by APP Factory')
    return app


web.run_app(app_factory(), host=config.host, port=config.port)
