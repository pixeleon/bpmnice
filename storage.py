import os

from dataclasses import dataclass

from sqlalchemy import create_engine, Column, Integer, String, Float, LargeBinary, DateTime, desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

FILES_TABLE_NAME = 'analysed_file'
RESULTS_TABLE_NAME = 'analysis_result'

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
    score: float = Column(Float, nullable=False)
    total_tasks: int = Column(Integer, nullable=False)
    invalid_tasks: int = Column(Integer, nullable=False)
    file_id: int = Column(Integer, nullable=False)
    created_time = Column(DateTime, server_default=func.now())


class AnalysedFile(Base):
    __tablename__ = FILES_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)


Base.metadata.create_all(engine)


def save_result(file_name, file_data, score, total_tasks, invalid_tasks):
    session = Session()
    try:
        file = AnalysedFile(name=file_name, data=file_data)
        session.add(file)
        session.flush()

        result = AnalysisResult(score=score, total_tasks=total_tasks, invalid_tasks=invalid_tasks, file_id=file.id)
        session.add(result)
        session.commit()
    except Exception as e:
        print(f"Failed to save analysis result to DB: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_results():
    session = Session()
    try:
        file_alias = aliased(AnalysedFile)
        results = session.query(
            AnalysisResult.id,
            AnalysisResult.total_tasks,
            AnalysisResult.invalid_tasks,
            AnalysisResult.score,
            file_alias.name.label("filename"),
        ).join(
            file_alias, AnalysisResult.file_id == file_alias.id
        ).order_by(desc(AnalysisResult.created_time)).limit(10).all()

        return results
    except Exception as e:
        print(f"Failed to retrieve analysis results from DB: {e}")
    finally:
        session.close()


def get_analysis_file(analysis_id):
    session = Session()
    analysis_result = session.query(AnalysisResult).filter_by(id=analysis_id).first()
    if analysis_result:
        file = session.query(AnalysedFile).filter_by(id=analysis_result.file_id).first()
        return file
    session.close()
