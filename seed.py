"""Utility file to seed ratings database from MovieLens data in seed_data/"""

# import datetime

from model import User, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for i, row in enumerate(open("HBFinalProject/seed_data/u.user")):
        row = row.rstrip()
        user_id, first_name, last_name = row.split("|")

        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_User()
    # load_User_Assets()
    # load_Positions()
