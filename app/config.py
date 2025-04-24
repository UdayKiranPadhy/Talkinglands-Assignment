from pydantic import BaseModel, Field

from pydantic_settings import BaseSettings


class CoreConfig(BaseSettings):
    service: str = Field(default="spatial-service")


class DbConfig(BaseSettings):
    host: str = Field(default="localhost")
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    database: str = Field(default="spatial_db")
    port: int = 5432

    class Config:
        env_prefix = "DB_"


class Config(BaseModel):
    """
    Loads application config from the environment using pydantic.BaseSettings, split up
    into different "modules" with different environment variable prefixes.
    """

    core: CoreConfig = Field(default_factory=lambda: CoreConfig())
    db: DbConfig = Field(default_factory=lambda: DbConfig())


_config: Config | None = None


class ConfigProvider:
    @classmethod
    def provide(cls, **_: dict[str, str]) -> Config:
        global _config
        if _config is not None:
            return _config

        _config = Config()
        return _config
