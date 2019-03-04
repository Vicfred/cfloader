from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker, load_only

from CodeforcesTables import Base, Codeforcer, RatingChange
import config

import codeforces


if __name__ == "__main__":
    dialect = "postgresql"
    username = config.DATABASE_CONFIG["user"]
    password = config.DATABASE_CONFIG["password"]
    host = config.DATABASE_CONFIG["host"]
    port = config.DATABASE_CONFIG["port"]
    dbname = config.DATABASE_CONFIG["dbname"]

    engine = create_engine(dialect + "://" + username + ":" + password + "@" + host + ":" + str(port) + "/" + dbname)

    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    user_handles = list()
    print("Fetching the list of users...")
    result = session.query(Codeforcer).options(load_only("handle"))
    for row in result:
        user_handles.append(row.handle)
        print(row.handle)
    print("Done fetching users.")

    for handle in user_handles:
        print(f"Fetching rating changes for user {handle}.")
        user_changes = codeforces.user_rating(handle)
        for user_change in user_changes:
            try:
                session.add(RatingChange(**vars(user_change)))
                session.commit()
            except (IntegrityError, InvalidRequestError):
                pass
            print(user_change)
        sleep(1/5)
    print("Done fetching all the users' rating changes.")
