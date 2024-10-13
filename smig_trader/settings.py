from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    debug: bool = False
    api_key: str = Field(..., env="ALPACA_PAPER_API_KEY")
    secret_key: str = Field(..., env="ALPACA_PAPER_SECRET_KEY")
    paper: bool = Field(True, env="ALPACA_PAPER_MODE")
    postgres_host: str = Field("db", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_user: str
    postgres_password: str
    postgres_db: str
    max_connections: int = 10
    timeout_seconds: int = 30

    @property
    def database_uri(self) -> str:
        """Assemble the Postgres database URI."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@localhost/{self.postgres_db}"

    class Config:
        env_prefix = ""
        # env_file = "../.env"
