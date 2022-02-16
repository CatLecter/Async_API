from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: str = Field('6379', env='REDIS_PORT')
    service_url: str = Field('http://127.0.0.1:80', env='SERVICE_URL')

    class Config:
        env_file = '.env'


config: TestSettings = TestSettings()
