from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, PrimaryKeyConstraint, Float, ARRAY, Enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy_utils import CompositeType, CompositeArray

from codeforces import *
from codeforces.Party import Party
from codeforces.Problem import Problem

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
    type = Column(ENUM(Contest.Type))  # TODO: Conflicts with problem type
    phase = Column(ENUM(Contest.Phase))
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


# TODO: enforce non null fields where possible
"""
class Submission(Base):
    __tablename__ = "submission"
    id = Column(Integer, primary_key=True)
    contestId = Column(Integer)
    creationTimeSeconds = Column(Integer)
    relativeTimeSeconds = Column(Integer)
    problem = Column(
        CompositeType(
            'problem',
            [
                Column('contestId', Integer),
                Column('problemsetName', String(256)),
                Column('index', String(256)),
                Column('name', String(256)),
                Column('type', Enum(Problem.Type)),  # BUG the type need to be created manually TODO conflict with contest type
                Column('points', Float),
                Column('rating', Integer),
                Column('tags', ARRAY(String(256)))
            ]
        )
    )
    author = Column(
        CompositeType(
            'party',
            [
                Column('contestId', Integer),
                # TODO use the composite type member
                # Column('members', CompositeArray(CompositeType('member', [Column('handle', String(256))]))),
                Column('members', ARRAY(String(256))),
                Column('participantType', ENUM(Party.ParticipantType)),  # BUG the type need to be created manually
                Column('teamId', Integer),
                Column('teamName', String(256)),
                Column('ghost', Boolean),
                Column('room', Integer),
                Column('startTimeSeconds', Integer)
            ]
        )
    )
    programmingLanguage = Column(String(256))
    verdict = Column(ENUM(Submission.Verdict))
    testset = Column(ENUM(Submission.TestSet))
    passedTestCount = Column(Integer)
    timeConsumedMillis = Column(Integer)
    memoryConsumedBytes = Column(Integer)
"""

dialect = "postgresql"
username = config.DATABASE_CONFIG["user"]
password = config.DATABASE_CONFIG["password"]
host = config.DATABASE_CONFIG["host"]
port = config.DATABASE_CONFIG["port"]
dbname = config.DATABASE_CONFIG["dbname"]
engine = create_engine(dialect + "://" + username + ":" + password + "@" + host + ":" + str(port) + "/" + dbname)

# BUG the type need to be created manually
# TODO BUG problem type conflicts with problem type, maybe that is causing this
#problem_type = ENUM(Problem.Type)
#problem_type.create(engine)
#participant_type = ENUM(Party.ParticipantType)
#participant_type.create(engine)

Base.metadata.create_all(engine)
