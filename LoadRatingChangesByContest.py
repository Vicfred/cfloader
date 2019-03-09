from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker

from CodeforcesTables import Base, RatingChange
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

    print("Fetching contest list.")
    contests = codeforces.contest_list(False)
    print(f"Done. Fetched {len(contests)} contests.")

    for contest in contests:
        sleep(1/5)
        rating_changes = codeforces.contest_ratingChanges(contest.id)
        if rating_changes is None:
            continue
        print(f"Processing rating changes for contest {contest.name} got {len(rating_changes)} changes.")
        rating_changes = [vars(item) for item in rating_changes]
        session.bulk_insert_mappings(RatingChange, rating_changes)
        session.commit()
