from dataclasses import dataclass
from typing import List

from flask_login import UserMixin
from sqlalchemy import Column, Integer, Float, DateTime, func, String, LargeBinary
from sqlalchemy.orm import declarative_base

USER_TABLE_NAME = 'app_user'
FILES_TABLE_NAME = 'analysed_file'
RESULTS_TABLE_NAME = 'analysis_result'

Base = declarative_base()


class AppUser(UserMixin, Base):
    __tablename__ = USER_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_time = Column(DateTime, server_default=func.now())


@dataclass
class AnalysisResult(Base):
    __tablename__ = RESULTS_TABLE_NAME
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    score: float = Column(Float, nullable=False)
    total_tasks: int = Column(Integer, nullable=False)
    invalid_tasks: int = Column(Integer, nullable=False)
    file_id: int = Column(Integer, nullable=False)
    user_id: int = Column(Integer, nullable=False)
    created_time = Column(DateTime, server_default=func.now())


class AnalysedFile(Base):
    __tablename__ = FILES_TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)

@dataclass
class LabelScore:
    label: str
    score: int


@dataclass
class AnalysisResultDto:
    filename: str
    score: float
    total_tasks: int
    invalid_tasks: int
    labels_score: List[LabelScore]
