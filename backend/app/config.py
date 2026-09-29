from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://querymind:querymind@localhost:5432/querymind"
    llm_api_key: str = ""
    llm_model: str = ""
    max_result_rows: int = 500
    query_timeout_seconds: int = 10
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
