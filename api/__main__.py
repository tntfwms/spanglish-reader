from logging import getLogger
from aiohttp import web
from typing import AsyncIterator
from aiohttp import ClientSession

from .routes import upload_api_page
import config
from .logs import setup_logging
setup_logging()

logger = getLogger('App Factory')

async def client_session_ctx(app: web.Application) -> AsyncIterator:
    logger.info('Creating ClientSession')
    app['client_session'] = ClientSession()

    yield

    logger.info('Closing ClientSession')
    await app['client_session'].close()


async def app_factory() -> web.Application:
    logger.info('Creating Application (entering APP Factory)')
    app = web.Application()

    logger.info('Adding Routes')
    app.add_routes(
        [
            web.post('/api/v1/upload', upload_api_page),
        ],
    )


    logger.info('Registering Cleanup contexts')
    app.cleanup_ctx.append(client_session_ctx)

    logger.info('APP is now prepared and can be returned by APP Factory')
    return app


web.run_app(app_factory(), host=config.host, port=config.port)
