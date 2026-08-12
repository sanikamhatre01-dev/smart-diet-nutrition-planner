from database.database import engine, Base
from database import models


def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully!")


if __name__ == "__main__":
    create_database()
