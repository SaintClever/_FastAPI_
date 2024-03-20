from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/tasks"
# DATABASE_URL = "mysql+mysqlconnector://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"

user = "root"
password = "****MySQL*"
database = "tasks"
host = "localhost"
port = 3306

# DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{port}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
