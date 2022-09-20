from sqlalchemy import create_engine
import config

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
# Change it for your AWS endpoint
ENDPOINT = config.endpoint
USER = 'postgres'
PASSWORD = config.password
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(
    f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")


if __name__ == "__main__":
    engine.connect()
