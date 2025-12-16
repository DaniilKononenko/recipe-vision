from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_PATH = Path(__file__).parent.parent
UPLOAD_DIR = BASE_PATH / "/tmp/uploads"   
STATIC_DIR = BASE_PATH / "static"
    

class OpenRouter(BaseModel):
    api_key: str
    api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    # api_url: str = "https://openrouter.ai/api/v1"
    model_id: str = "openrouter/bert-nebulon-alpha"


class Server(BaseModel):
    host: str = "localhost"
    port: int = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_PATH / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    open_router: OpenRouter
    server: Server = Server()


settings = Settings()


if __name__ == "__main__":
    print(settings.open_router.api_key)