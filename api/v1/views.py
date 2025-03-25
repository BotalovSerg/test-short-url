from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from .schemas import UrlRequest
from .utils import get_short_url

router = APIRouter(tags=["API v1"])

url_storage = {}


@router.post("/")
async def create_url(request: UrlRequest):
    """
    POST / - Создание сокращенного URL.

    Принимает JSON с полем "url", содержащим оригинальный URL.
    Генерирует уникальный идентификатор для сокращенного URL и сохраняет соответствие между ними.

    Входные данные:
        {
            "url": "string"  # Оригинальный URL (обязательное поле)
        }

    Выходные данные:
        {
            "message": "ID: <short_url_id>, URL: <original_url>",
            "status_code": 201
        }

    Возможные ошибки:
        - 400 Bad Request: Если поле "url" отсутствует или пустое.
    """
    original_url = request.url.strip()
    if not original_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    short_url_id = get_short_url(original_url)
    url_storage[short_url_id] = original_url
    return {"message": f"ID: {short_url_id}, URL: {original_url}", "status_code": 201}


@router.get("/{url_id}")
async def redirect_to_original(url_id: str):
    """
    GET /<url_id> - Перенаправление на исходный URL.
    
    Принимает идентификатор сокращенного URL в качестве параметра пути.
    Если идентификатор найден, выполняет перенаправление на соответствующий исходный URL.
    
    Параметры пути:
        url_id (str): Идентификатор сокращенного URL.
    
    Ответ:
        - Код ответа: 307 Temporary Redirect.
        - Заголовок Location: Исходный URL.
    
    Возможные ошибки:
        - 404 Not Found: Если идентификатор сокращенного URL не найден.
    """
    original_url = url_storage.get(url_id)
    if original_url is None:
        raise HTTPException(status_code=404, detail="Shortened URL not found")

    return RedirectResponse(url=original_url, status_code=307)
