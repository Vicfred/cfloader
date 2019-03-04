from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import config

Base = declarative_base()


class Codeforcer(Base):
    __tablename__ = 'codeforcer'
    handle = Column(String(250), primary_key=True)
    email = Column(String(1024))
    vkId = Column(String(1024))
    openId = Column(String(250))
    firstName = Column(String(250))
    lastName = Column(String(250))
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


class RatingChange(Base):
    __tablename__ = 'rating_change'
    contestId = Column(Integer, primary_key=True)
    contestName = Column(String(250))
    handle = Column(String(250), ForeignKey('codeforcer.handle'))
    rank = Column(Integer)
    ratingUpdateTimeSeconds = Column(Integer)
    oldRating = Column(Integer)
    newRating = Column(Integer)
    codeforcer = relationship(Codeforcer)


dialect = "postgresql"
username = config.DATABASE_CONFIG['user']
password = config.DATABASE_CONFIG['password']
host = config.DATABASE_CONFIG['host']
port = config.DATABASE_CONFIG['port']
dbname = config.DATABASE_CONFIG['dbname']
engine = create_engine(dialect+'://'+username+":"+password+"@"+host+":"+str(port)+"/"+dbname)

Base.metadata.create_all(engine)
