#!/usr/bin/env python3
"""User model definition for the 'users' table """


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class User(Base):
    """User model

    Represents a user in the database.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


# This part provide some visible output
if __name__ == '__main__':
    print(f"Table name: {User.__tablename__}")
    print("Columns:")
    for column in User.__table__.columns:
        print(f"{column.name}: {column.type}")    
