from pydantic_settings import BaseSettings

class settings(BaseSettings):

    


    App_name: str 
    App_version: str

    FILE_ALLOWED_EXTENSIONS: set[str] = {"application/pdf", "text/plain"}
    FILE_MAX_SIZE: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int =1000
    


    class Config:
        env_file = "src/.env"


def get_settings():
    return settings()