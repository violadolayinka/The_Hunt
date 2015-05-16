"""Utility file to seed ratings database from MovieLens data in seed_data/"""

# import datetime

from model import User, Position, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id, first_name, last_name = row.split("|")

        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name)

        # This adds my user to the session
        db.session.add(user)

        # This provide some sense of progress
        if i % 100 == 0:
            print i

    # This commits my user to the database User
    db.session.commit()


def load_positions():
    """Load position from u.position into database."""

    print "Position"

    for i, row in enumerate(open("seed_data/u.position")):
        row = row.rstrip()
        position_id, title, position_summary, company_name, location, application_status, position_url = row.split("|")

        position = Position(position_id=position_id,
                            title=title,
                            position_summary=position_summary,
                            company_name=company_name,
                            location=location,
                            application_status=application_status,
                            position_url=position_url)
        # print title

        # This adds my position to the session
        db.session.add(position)

        # This provide some sense of progress
        if i % 100 == 0:
            print i

    # This commits my position to the database User
    db.session.commit()


def load_user_assets():
    """Load User's Assets from u.user_assets into database."""

    print "User_Assets"

    for i, row in enumerate(open("seed_data/u.user_assets")):
        row = row.rstrip()
        user_asset_id, asset_type, asset_content = row.split("|")

        user_assets = User_Assets(user_asset_id=user_asset_id,
                                asset_type=asset_type,
                                asset_content=asset_content)
        # print title

        # This adds my position to the session
        db.session.add(user_assets)

        # This provide some sense of progress
        if i % 100 == 0:
            print i

    # This commits my position to the database User
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_user_assets()
    load_positions()
