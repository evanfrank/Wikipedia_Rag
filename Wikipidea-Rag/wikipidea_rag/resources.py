from sqlalchemy import create_engine
from dagster import ConfigurableResource
from sqlalchemy.engine.base import Engine


class postgres_con(ConfigurableResource):
    password: str

    def make_con(self) -> Engine:
        user = "surf_app"
        pwd = self.password
        host = "localhost"
        db = "wikipedia_rag"
        con_string = f"postgresql+psycopg2://{user}:{pwd}@{host}/{db}"
        engine = create_engine(con_string)
        return engine
