# this script takes about 23.6 minutes to run on all no-gym contests (1135 contests as of 13-Jul-2019 sleep(1/5)
# this script takes about 21.5 minutes to run on all no-gym contests (1138 contests as of 25-Jul-2019 sleep(1/10)
# this script takes about 19.7 minutes to run on all no-gym contests (1147 contests as of 25-Jul-2019 sleep(1/10)
import time
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

    t0 = time.time()
    for contest in contests:
        sleep(1/20)
        rating_changes = codeforces.contest_ratingChanges(contest.id)
        if rating_changes is None:
            continue
        print(f"Processing rating changes for contest {contest.name} got {len(rating_changes)} changes.")
        rating_changes = [vars(item) for item in rating_changes]
        session.bulk_insert_mappings(RatingChange, rating_changes)
        session.commit()
    print(f"It took {time.time() - t0} seconds.")
