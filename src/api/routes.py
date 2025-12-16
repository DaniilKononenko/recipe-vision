import json

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status,
    Request
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.utils import send_image_analize_request, send_recipe_request


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request":request, "title": "Главная"}
    )

@router.post("/api/upload-photo")
async def upload_photo(image: UploadFile = File(...)):
    if image.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format"
        )

    ingredients = await send_image_analize_request(image)

    recipes = await send_recipe_request(json.dumps(ingredients))

    result = {
        "ingredients": ingredients["products"],
        "recipes": recipes["recipes"]
    }

    return result