from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "OpsBoard"
    env: str = os.getenv("APP_ENV", "dev")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_anon_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()
