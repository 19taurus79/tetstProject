from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://admin:root@localhost:5432/test_db")


if __name__ == "__main__":
    print(engine)
