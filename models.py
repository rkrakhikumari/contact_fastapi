from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class Contact(Base):
    __tablename__ ='contact'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone_num = Column(String)
    note = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))  



    