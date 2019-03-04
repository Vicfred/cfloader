from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    handle = Column(String, primary_key=True)
    email = Column(String(1024))
    vkId = Column(String(1024))
    openId = Column(String(250))
    firstName = Column(String(250))
    secondName = Column(String(250))
    country = Column(String(250))
    city = Column(String(250))
    organization = Column(String(250))
    contribution = Column(Integer)
    rank = Column(String(250))
    rating = Column(Integer)
    maxRank = Column(String(250))
    maxRating = Column(Integer)
    lastOnlineTimeSeconds = Column(Integer)
    registrationTimeSeconds = Column(Integer)
    friendOfCount = Column(Integer)
    avatar = Column(String(1024))
    titlePhoto = Column(String(1024))


engine = create_engine('sqlite:///sqlalchemy_example.db')

Base.metadata.create_all(engine)
