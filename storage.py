import os

from dataclasses import dataclass

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

RESULTS_TABLE_NAME = 'nlss_result'

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
schema = os.getenv("DATABASE_NAME")
host = os.getenv("DATABASE_HOST")
ssl_ca = os.getenv("DATABASE_SSL_CA")

db_url = f"mysql+pymysql://{username}:{password}@{host}:3306/{schema}"
ssl_config = {"ssl": {"ssl_ca": ssl_ca}}

engine = create_engine(db_url, connect_args=ssl_config)

Session = sessionmaker(bind=engine)
Base = declarative_base()


@dataclass
class AnalysisResult(Base):
    __tablename__ = RESULTS_TABLE_NAME
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    filename: str = Column(String(255), nullable=False)
    score: float = Column(Float, nullable=False)
    total_tasks: int = Column(Integer, nullable=False)
    invalid_tasks: int = Column(Integer, nullable=False)


Base.metadata.create_all(engine)


def save_result(filename, score, total_tasks, invalid_tasks):
    session = Session()
    try:
        result = AnalysisResult(filename=filename, score=score, total_tasks=total_tasks, invalid_tasks=invalid_tasks)
        session.add(result)
        session.commit()
    except Exception as e:
        print(f"Failed to save result to DB: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_results():
    session = Session()
    try:
        results = session.query(AnalysisResult).all()
        return results
    except Exception as e:
        print(f"Failed to retrieve results from DB: {e}")
    finally:
        session.close()
