from pathlib import Path

from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    ELASTIC_HOST: str = Field("http://127.0.0.1", env="ELASTIC_HOST")
    ELASTIC_PORT: str = Field("9200", env="ELASTIC_PORT")
    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: str = Field("6379", env="REDIS_PORT")
    SERVICE_URL: str = Field("http://127.0.0.1:8000", env="SERVICE_URL")

    expected_responses_dir: Path = Field("functional/testdata/expected")
    indexes_dir: Path = Field("functional/testdata/indexes")
    data_dir: Path = Field("functional/testdata/data_for_indexes")

    class Config:
        env_file = ".env"


config: TestSettings = TestSettings()
