from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SubIds(Base):
    __tablename__ = 'Subscriptions Info'
    id = Column(Integer, primary_key=True)
    sub_name = Column(String(255))
    price = Column(Integer)
    date = Column(Date)
