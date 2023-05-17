from aiohttp.web import Request, Response, FileResponse
import random, asyncio
from logging import getLogger
from json import JSONDecodeError, dumps as dump_json
import base64

from .raw import render as render_text
import config

log = getLogger('routes')

def generate_id() -> str:
    return ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm', k=random.randint(10, 20)))

ResType = Response | FileResponse

def response(data: dict, status: int, headers: dict[str, str]) -> Response:
    headers['Access-Control-Allow-Origin'] = f'https://{config.gh_name}.github.io' if config.custom_domain is None else config.custom_domain
    return Response(
        body=dump_json(data), status=status, headers=headers
    )

async def upload_api_page(res: Request) -> ResType:
    log.info(f"Received request from {res.remote} to {res.method} {res.path}")

    try:
        data = await res.json()
    except JSONDecodeError:
        print(await res.text())
        return Response(body=dump_json({'error' : 'Invalid JSON Given', 'success' : False}), status=400)
    text = data.get("text")

    if text is None:
        return Response(body=dump_json({'error' : 'Invalid JSON Data Given. Expected `text` key.', 'success' : False}), status=400)
    
    id = generate_id()
    try:
        final = await asyncio.to_thread(render_text, text.strip("\n"))
    except Exception as e:
        return Response(body=dump_json({'success' : False, 'error' : str(e)}), status=400)

    url = f"https://api.github.com/repos/{config.gh_name}/{config.gh_repo}/contents/docs/read/{id}.html"
    headers = {
        'accept' : 'application/vnd.github+json' 
    }
    data = {
        'message' : f"Upload Spanglish From Page",
        "content" : base64.b64encode(final.encode('utf-8')).decode()
    }
    async with res.app['client_session'].get(url, headers=headers, json=data) as response:
        return_data = await response.text()
        print(return_data)
    
    return Response(body=dump_json({'success' : True, 'id' : id}), status=201)
