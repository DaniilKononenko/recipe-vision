import aiohttp, json, base64, re
from fastapi import HTTPException, UploadFile
from src.consts import CV_PROMT, RECIPE_PROMT
from src.config import settings, UPLOAD_DIR


async def send_image_analize_request(image: UploadFile):

    image_bytes = await image.read()  # ✅ читаем только один раз

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "model": settings.open_router.model_id,
        "messages": [
             {
                "role": "system",
                "content": CV_PROMT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image.content_type};base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {settings.open_router.api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Image Analysis"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.open_router.api_url,
            json=payload,  # ✅ теперь правильно
            headers=headers
        ) as resp:
            result = json.loads(await resp.text())

            if resp.status != 200:
                print(result)
                raise HTTPException(status_code=resp.status, detail=result)
            
            data = result["choices"][0]["message"]["content"]
            match = re.search(r"```json\s*(\{.*\})\s*```", data, re.DOTALL)
            if match:
                json_text = match.group(1)
            else:
                # если нет блоков, пробуем использовать как есть
                json_text = data
                
            # 2. Парсим JSON
            return json.loads(json_text)
        

async def send_recipe_request(ingredients: str):
    payload = {
        "model": settings.open_router.model_id,
        "messages": [
            {
                "role": "system",
                "content": RECIPE_PROMT
            },
            {
                "role": "user",
                "content": ingredients
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {settings.open_router.api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "Getting recipe"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            settings.open_router.api_url,
            json=payload,  # ✅ теперь правильно
            headers=headers
        ) as resp:
            result = json.loads(await resp.text())

            if resp.status != 200:
                print(result)
                raise HTTPException(status_code=resp.status, detail=result)
            

            data = result["choices"][0]["message"]["content"]
            match = re.search(r"```json\s*(\{.*\})\s*```", data, re.DOTALL)
            if match:
                json_text = match.group(1)
            else:
                # если нет блоков, пробуем использовать как есть
                json_text = data

            # 2. Парсим JSON
            return json.loads(json_text)