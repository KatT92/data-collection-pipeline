from sqlalchemy import create_engine

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
# Change it for your AWS endpoint
ENDPOINT = 'bgg-data-1.cbx9lvymwfei.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = 'MjvJr2sU7SWDShj'
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(
    f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")


if __name__ == "__main__":
    engine.connect()
