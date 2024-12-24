from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as database:
        yield database