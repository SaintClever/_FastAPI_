import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv(".env")

localhost: str = os.getenv("LOCALHOST")
database: str = os.getenv("DATABASE")
username: str = os.getenv("USERNAME")
password: str = os.getenv("PASSWORD")

DATABASE_URL = f"postgresql://{username}:{password}@{localhost}/{database}"

engine = create_engine(DATABASE_URL)


def get_session():
    with engine.connect() as connection:
        with Session(connection) as session:
            yield session
