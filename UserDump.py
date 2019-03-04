from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from CodeforcesTables import Codeforcer, Base
import config
import json


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

    print("Fetching users...")
    with open('user.ratedList', mode="r", encoding="utf-8") as f:
        data = json.load(f)
    print("====================Done fetching users==========================")

    users = list()
    for x in data["result"]:
        users.append(x)

    for user in users:
        print(user)
    print(len(users))

    session.bulk_insert_mappings(Codeforcer, users)
    session.commit()

    print("Done inserting into DB :D")
