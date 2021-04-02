import os

import aiohttp
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer

security = HTTPBearer()

session = aiohttp.ClientSession()


async def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    url = os.getenv('AUTH_SERVICE_URL')
    async with session.get(url, headers={'Authorization': credentials.credentials}) as response:
        if response.status == 401:
            raise HTTPException(status_code=401)
