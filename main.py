import uvicorn
from fastapi import FastAPI

import functions
from minecraft_server import MinecraftServer

app = FastAPI()


@app.get('/minecraft/start/{server_name}')
async def start_server(server_name: str):
    return f'Starting {server_name}'


@app.get('/minecraft/stop/{server_name}')
async def stop_server(server_name: str):
    return f'Stopping {server_name}'


@app.get('/minecraft/restart/{server_name}')
async def restart_server(server_name: str):
    await stop_server(server_name)
    await start_server(server_name)
    return f'Restarting {server_name}'


@app.get('/minecraft/status/{server_name}')
async def status_server(server_name: str):
    return f'Status of {server_name}'


if __name__ == '__main__':
    uvicorn.run(app, host='')
