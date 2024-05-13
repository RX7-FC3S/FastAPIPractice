from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///sqlite.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_all_tables():
    SQLModel.metadata.create_all(engine)


def create_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
