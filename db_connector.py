from sqlalchemy import create_engine, text

import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
schema = os.getenv("DB_SCHEMA")
host = os.getenv("DB_HOST")
ssl_ca = os.getenv("SSL_CA_PATH")

db_url = f"mysql+pymysql://{username}:{password}@{host}:3306/{schema}"

ssl_config = {"ssl": {"ssl_ca": ssl_ca}}

engine = create_engine(db_url, connect_args=ssl_config)


def get_all_results():
    with engine.connect() as conn:
        result = conn.execute(text("select * from analysis_result"))
        rows = [row._asdict() for row in result]
        return rows