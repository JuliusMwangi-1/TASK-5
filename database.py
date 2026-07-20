from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:MyRealPassword@localhost:5432/music_store"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
<<<<<<< HEAD
        db.close()
=======
        db.close()
>>>>>>> 26687e4fd591bee1d22d307f372226e2b7518d08
