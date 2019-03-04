from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from codeforces import *

import config

Base = declarative_base()


# TODO: enforce non null fields where possible
class Codeforcer(Base):
    __tablename__ = "codeforcer"
    handle = Column(String(256), primary_key=True)
    email = Column(String(1024))
    vkId = Column(String(1024))
    openId = Column(String(256))
    firstName = Column(String(256))
    lastName = Column(String(256))
    country = Column(String(256))
    city = Column(String(256))
    organization = Column(String(256))
    contribution = Column(Integer)
    rank = Column(String(256))
    rating = Column(Integer)
    maxRank = Column(String(256))
    maxRating = Column(Integer)
    lastOnlineTimeSeconds = Column(Integer)
    registrationTimeSeconds = Column(Integer)
    friendOfCount = Column(Integer)
    avatar = Column(String(1024))
    titlePhoto = Column(String(1024))


# TODO: enforce non null fields where possible
class Contest(Base):
    __tablename__ = "contest"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    type = Column(Enum(Contest.Type))
    phase = Column(Enum(Contest.Phase))
    frozen = Column(Boolean)
    durationSeconds = Column(Integer)
    startTimeSeconds = Column(Integer)
    relativeTimeSeconds = Column(Integer)
    preparedBy = Column(String(256))
    websiteUrl = Column(String(256))
    description = Column(String(1048576))
    difficulty = Column(Integer)
    kind = Column(String(256))
    icpcRegion = Column(String(256))
    country = Column(String(256))
    city = Column(String(256))
    season = Column(String(256))


# TODO: enforce non null fields where possible
class RatingChange(Base):
    __tablename__ = "rating_change"
    __table_args__ = (
        PrimaryKeyConstraint("contestId",
                             "contestName",
                             "handle",
                             "rank",
                             "ratingUpdateTimeSeconds",
                             "oldRating",
                             "newRating"),
    )
    contestId = Column(Integer)
    contestName = Column(String(256))
    handle = Column(String(256), ForeignKey("codeforcer.handle"))
    rank = Column(Integer)
    ratingUpdateTimeSeconds = Column(Integer)
    oldRating = Column(Integer)
    newRating = Column(Integer)
    codeforcer = relationship(Codeforcer)


dialect = "postgresql"
username = config.DATABASE_CONFIG["user"]
password = config.DATABASE_CONFIG["password"]
host = config.DATABASE_CONFIG["host"]
port = config.DATABASE_CONFIG["port"]
dbname = config.DATABASE_CONFIG["dbname"]
engine = create_engine(dialect + "://" + username + ":" + password + "@" + host + ":" + str(port) + "/" + dbname)

Base.metadata.create_all(engine)
