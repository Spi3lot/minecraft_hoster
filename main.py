import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse

from minecraft_server import MinecraftServer

app = FastAPI()
favicon_url = 'https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/favicon-96x96.png'
wpad_code = 'function FindProxyForURL(url, host) { return "DIRECT"; }'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')


@app.get('/wpad.dat', include_in_schema=False)
async def wpad():
    return wpad_code


@app.get('/minecraft/start/{server_name}')
async def start_server(server_name: str):
    if MinecraftServer.of(server_name).start():
        return f'Starting {server_name}'

    return MinecraftServer.NOT_FOUND_MESSAGE


@app.get('/minecraft/stop/{server_name}')
async def stop_server(server_name: str):
    if MinecraftServer.of(server_name).stop():
        return f'Stopping {server_name}'

    return MinecraftServer.NOT_FOUND_MESSAGE


@app.get('/minecraft/restart/{server_name}')
async def restart_server(server_name: str):
    if MinecraftServer.of(server_name).restart():
        return f'Restarting {server_name}'

    return MinecraftServer.NOT_FOUND_MESSAGE


@app.get('/minecraft/status/{server_name}')
async def status_server(server_name: str):
    return MinecraftServer.of(server_name).get_status()


if __name__ == '__main__':
    uvicorn.run(app, host='', port=80)
