# DONT USE, USE BY CONTEST INSTEAD
from time import sleep

import redis
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

    r = redis.Redis(host='localhost', port=6379, db=0)

    print("Fetching the list of users...")
    redis_key = "codeforces:handles:changes"
    if r.llen(redis_key) == 0:
        result = session.query(Codeforcer).options(load_only("handle"))
        for row in result:
            r.lpush(redis_key, row.handle)
            print(row.handle)
    print("Done fetching users.")

    while r.llen(redis_key) > 0:
        handle = r.rpop(redis_key).decode("utf-8")
        print(f"Fetching rating changes for user {handle}.")
        user_changes = list()
        try:
            user_changes = codeforces.user_rating(handle)
            sleep(1/5)
        except:
            r.lpush(redis_key, handle)
            continue
            pass
        if user_changes is None:
            r.lpush(redis_key, handle)
            continue
        for user_change in user_changes:
            try:
                session.add(RatingChange(**vars(user_change)))
                session.commit()
            except (IntegrityError, InvalidRequestError):
                pass
            print(user_change)
        r.save()
    print("Done fetching all the users' rating changes.")
