from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    String,
    Integer,
    CHAR,
    Float,
    Boolean,
)
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"
    userID = Column("ID ", Integer, primary_key=True)
    username = Column("FirstName", String)
    age = Column("Age", Integer)
    sex = Column("Sex", String)
    bmi = Column("BMI", Float)
    children = Column("Number of Children", Integer)
    smoker = Column("smoker?", Boolean)
    region = Column("region", String)

    def __init__(self, userID, username, age, sex, bmi, children, smoker, region):
        self.userID = userID
        self.username = username
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
        self.region = region

    def __repr__(self):
        return f"({self.userID})"


engine = create_engine("sqlite:///new_database.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add a Person instance and commit changes
try:
    person = Person(1, "abhy", 18, "male", 23.1, 2, False, "north")
    session.add(person)
    session.commit()
    print("Person added successfully.")
except Exception as e:
    session.rollback()
    print("Error occurred while adding person:", e)
finally:
    session.close()
results = session.query(Person).all()
print("\n\n\n\n\n")
print(results)
