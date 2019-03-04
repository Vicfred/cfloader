from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from CodeforcesTables import Codeforcer, Base
import config

from codeforces import *


if __name__ == "__main__":
    dialect = "postgresql"
    username = config.DATABASE_CONFIG['user']
    password = config.DATABASE_CONFIG['password']
    host = config.DATABASE_CONFIG['host']
    port = config.DATABASE_CONFIG['port']
    dbname = config.DATABASE_CONFIG['dbname']

    engine = create_engine(dialect + '://' + username + ":" + password + "@" + host + ":" + str(port) + "/" + dbname)

    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


