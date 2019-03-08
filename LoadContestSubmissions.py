from time import sleep

from dataclasses import astuple
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

    contests = codeforces.contest_list(False)

    for contest in contests:
        sleep(1/5)
        # only processing submissions for official contests
        submissions = codeforces.contest_status(contest.id)
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
