from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    
    try:
        # connection = engine.connect()
        # print('DB connected successfully', connection)
        yield db
    finally:
        db.close()

# if __name__ == "__main__":
#     # Consumir el generador para verificar la conexión
#     db_gen = get_db()
#     next(db_gen)  # Esto ejecuta el bloque try y verifica la conexión