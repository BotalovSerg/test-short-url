import aiohttp


from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse


from .schemas import UrlRequest

router = APIRouter(tags=["API v1"])

url_storage = {}


@router.post("/")
async def create_url(request: UrlRequest):
    """
    Принимает JSON с полем "url".
    """
    original_url = request.url.strip()
    if not original_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    short_url_id = original_url[0] + str(len(original_url)) + original_url[-1]
    url_storage[short_url_id] = original_url
    print(url_storage)
    return {"message": f"ID: {short_url_id}, URL: {original_url}", "status_code": 201}


@router.get("/{url_id}")
async def redirect_to_original(url_id: str):
    """
    GET /<url_id> - Вернуть исходный URL.
    Принимает идентификатор сокращенного URL и перенаправляет на исходный URL.
    """
    print(url_id)
    original_url = url_storage.get(url_id)
    if original_url is None:
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    return RedirectResponse(url=original_url, status_code=307)


@router.post("/async-fetch")
async def async_fetch(request: Request):
    """
    Асинхронный запрос на внешний сервис.
    Принимает JSON с полем "url" и возвращает данные, полученные от внешнего сервиса.
    """
    try:
        body = await request.json()
        external_url = body.get("url")
        if not external_url:
            raise HTTPException(status_code=400, detail="External URL is required")

        async with aiohttp.ClientSession() as session:
            async with session.get(external_url) as response:
                data = await response.text()
                return {"data": data, "status_code": response.status}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during async fetch: {str(e)}"
        )
