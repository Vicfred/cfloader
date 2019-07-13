from time import sleep

import redis
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker

from CodeforcesTables import Base, Submission
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

    print("Fetching contest list...")
    redis_key = "codeforces:handles:changes"
    if r.llen(redis_key) == 0:
        contests = codeforces.contest_list(False)
        for contest in contests:
            r.lpush(redis_key, contest.id)
        print(f"Got {len(contests)} contests.")

    contest_submissions = list()
    while r.llen(redis_key) > 0:
        contest_id = r.rpop(redis_key).decode("utf-8")
        sleep(1/5)
        # only processing submissions for official contests
        print("Fetching submissions...")
        try:
            submissions = codeforces.contest_status(contest_id)
        except:
            print(f"Fetching failed for contest_id: {contest_id}.")
            r.lpush(redis_key, contest_id)
            continue
            pass
        print("Done.")
        print(f"Submission list length: {len(contest_submissions)}")
        if submissions is None:
            print(f"Skipping contest {contest_id}.")
            continue
        print(f"Processing submissions for contest {contest_id}, got {len(submissions)} submissions.")
        for submission in submissions:
            problem = submission.problem
            problem.type = problem.type.name
            # needs the ordered tuple
            submission.problem = (
                problem.contestId,
                problem.problemSetName,
                problem.index,
                problem.name,
                problem.type,
                problem.points,
                problem.rating,
                problem.tags
            )
            author = submission.author
            author.participantType = author.participantType.name
            # saving only the handles as string instead of objects
            handles = list()
            for member in author.members:
                handles.append(member.handle)
            author.members = handles
            # needs the ordered tuple
            submission.author = (
                author.contestId,
                author.members,
                author.participantType,
                author.teamId,
                author.teamName,
                author.ghost,
                author.room,
                author.startTimeSeconds
            )
            contest_submissions.append(vars(submission))
        if len(contest_submissions) > 1_000_000:
            try:
                print(f"Inserting {len(contest_submissions)} submissions.")
                session.bulk_insert_mappings(Submission, contest_submissions)
                session.commit()
                print("Done inserting. :D")
                contest_submissions = list()
            except (IntegrityError, InvalidRequestError):
                print("Something went wrong, not inserting :<")

                for contest_submission in contest_submissions:
                    try:
                        session.add(Submission, **contest_submission)
                        session.commit()
                    except (IntegrityError, InvalidRequestError):
                        continue
                contest_submissions = list()
                continue
                pass
