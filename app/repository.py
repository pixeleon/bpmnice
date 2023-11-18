import os

from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker, aliased
from werkzeug.security import generate_password_hash, check_password_hash

from app.model import AppUser, AnalysedFile, AnalysisResult, Base

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
schema = os.getenv("DATABASE_NAME")
host = os.getenv("DATABASE_HOST")
ssl_ca = os.getenv("DATABASE_SSL_CA")

db_url = f"mysql+pymysql://{username}:{password}@{host}:3306/{schema}"
ssl_config = {"ssl": {"ssl_ca": ssl_ca}}

engine = create_engine(db_url, connect_args=ssl_config)

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def save_app_user(name, email, password):
    session = Session()
    try:
        if not session.query(AppUser).filter_by(email=email).first():
            user = AppUser(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
            session.add(user)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Failed to save new user to DB: {e}")
        session.rollback()
    finally:
        session.close()


def get_app_user_by_credentials(email, password):
    with Session() as session:
        user = session.query(AppUser).filter_by(email=email).first()
        return user if (user and check_password_hash(user.password, password)) else None


def get_app_user_by_id(id):
    with Session() as session:
        user = session.query(AppUser).get(id)
        return user


def save_result(file_name, file_data, score, total_tasks, invalid_tasks, user_id):
    session = Session()
    try:
        file = AnalysedFile(name=file_name, data=file_data)
        session.add(file)
        session.flush()

        result = AnalysisResult(
            score=score,
            total_tasks=total_tasks,
            invalid_tasks=invalid_tasks,
            user_id=user_id,
            file_id=file.id
        )

        session.add(result)
        session.commit()
    except Exception as e:
        print(f"Failed to save analysis result to DB: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_results(user_id):
    session = Session()
    try:
        file_alias = aliased(AnalysedFile)
        results = session.query(
            AnalysisResult.id,
            AnalysisResult.total_tasks,
            AnalysisResult.invalid_tasks,
            AnalysisResult.score,
            AnalysisResult.created_time,
            file_alias.name.label("filename"),
        ).filter_by(user_id=user_id).join(file_alias, AnalysisResult.file_id == file_alias.id).order_by(
            desc(AnalysisResult.created_time)).all()
        return results
    except Exception as e:
        print(f"Failed to retrieve analysis results from DB: {e}")
    finally:
        session.close()


def get_results_page(user_id, page=1, page_size=10):
    session = Session()
    try:
        file_alias = aliased(AnalysedFile)
        offset = (page - 1) * page_size
        results = session.query(
            AnalysisResult.id,
            AnalysisResult.score,
            AnalysisResult.total_tasks,
            AnalysisResult.invalid_tasks,
            AnalysisResult.created_time,
            file_alias.name.label("filename"),
        ).filter_by(user_id=user_id).join(file_alias, AnalysisResult.file_id == file_alias.id).order_by(
            desc(AnalysisResult.created_time)).offset(offset).limit(page_size).all()
        return results
    except Exception as e:
        print(f"Failed to retrieve analysis results page from DB: {e}")
    finally:
        session.close()


def get_results_count(user_id):
    with Session() as session:
        return session.query(func.count(AnalysisResult.id)).filter_by(user_id=user_id).scalar()


def get_analysis_file(analysis_id):
    with Session() as session:
        analysis_result = session.query(AnalysisResult).filter_by(id=analysis_id).first()
        if analysis_result:
            file = session.query(AnalysedFile).filter_by(id=analysis_result.file_id).first()
            return file
