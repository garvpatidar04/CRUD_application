from sqlalchemy import create_engine
from .config import settings
from alembic.config import Config
from alembic import command

engine = create_engine(url=settings.database_url)

def talk(engine=engine):
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print('DB connection established')

        alembic_cnfg = Config("alembic.ini")

        try:
            print("Checking the alembic migrations")
            with engine.connect() as conn:
                result = conn.execute("SELECT version_num FROM alembic_version")
                current_version = result.scalar()
                print(f"Current migration version of db: {current_version}")
        except Exception as e:
            print("No migration history found. Running migrations...")
            command.upgrade(alembic_cnfg, "head")  
            print("Migrations applied successfully.")

    except Exception as e:
        print(f"Error during connecting to db, {e}")
        raise

# if __name__=="__main__":
#     print("Running database migrations...")
#     talk(engine)
#     print("Migrations completed. Now starting FastAPI server...")