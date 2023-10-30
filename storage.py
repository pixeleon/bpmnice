from sqlalchemy import create_engine, text

import os

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
schema = os.getenv("DATABASE_NAME")
host = os.getenv("DATABASE_HOST")
ssl_ca = os.getenv("DATABASE_SSL_CA")

db_url = f"mysql+pymysql://{username}:{password}@{host}:3306/{schema}"

ssl_config = {"ssl": {"ssl_ca": ssl_ca}}

engine = create_engine(db_url, connect_args=ssl_config)


def get_all_results():
    with engine.connect() as conn:
        result = conn.execute(text("select * from analysis_result"))
        rows = [row._asdict() for row in result]
        return rows