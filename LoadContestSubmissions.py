from time import sleep

from dataclasses import astuple
from http.client import IncompleteRead
from requests.exceptions import ChunkedEncodingError
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from urllib3.exceptions import ProtocolError

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

    print("Fetching contest list...")
    contests = codeforces.contest_list(False)
    print(f"Got {len(contests)} contests.")

    for contest in contests:
        sleep(1/5)
        # only processing submissions for official contests
        print("Fetching submissions...")
        try:
            submissions = codeforces.contest_status(contest.id)
        except (ChunkedEncodingError, ProtocolError, IncompleteRead):
            print(f"Fetching failed for contest {contest}, please requeue.")
            pass
        print("Done.")
        if submissions is None:
            print(f"Skipping contest {contest}.")
            continue
        print(f"Processing rating changes for contest {contest.name}, got {len(submissions)} submissions.")
        contest_submissions = list()
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
        try:
            print(f"Inserting {len(contest_submissions)} submissions.")
            session.bulk_insert_mappings(Submission, contest_submissions)
            session.commit()
            print("Done inserting. :D")
        except (IntegrityError, InvalidRequestError):
            print("Something went wrong, not inserting :<")
            pass
