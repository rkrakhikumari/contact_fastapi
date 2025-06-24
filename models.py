from database import Base
from sqlalchemy import Column, String, Integer

class Contact(Base):
    __tablename__ ='contact'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone_num = Column(String)
    note = Column(String)