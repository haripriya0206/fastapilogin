from sqlalchemy import Column, Integer, String
from database import Base


class Userdata(Base):
    __tablename__ = "userdata" 
    id= Column(Integer , nullable=False, primary_key=True)
    username = Column(String(100),nullable=True) 
    email =  Column(String(100), nullable=True)
    password = Column(String(100),nullable=True)


    def __repr__(self):
        return '<Userdata %r>' %(self.id)