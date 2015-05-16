"""Models and database functions for HB Spring 2015 Final project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions
class User(db.Model):
    """User"""

    __tablename__ = "User"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(100))
    email_address = db.Column(db.String(100))
    last_login = db.Column(db.Date)
    user_LinkedIn_url = db.Column(db.String(100))
    user_Twitter_url = db.Column(db.String(100))
    user_Facebook_url = db.Column(db.String(100))
    user_website_url = db.Column(db.String(100))


class Position(db.Model):
    """User's Positions"""

    __tablename__ = "Position"

    position_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50))
    position_summary = db.Column(db.String(300))
    deadline = db.Column(db.DateTime)
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    application_status = db.Column(db.String(50))
    position_url = db.Column(db.String(100))


class User_Assets(db.Model):
    """User's Job Applicaton Assets."""

    __tablename__ = "User_Assets"

    user_asset_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    asset_type = db.Column(db.String(100))
    asset_content = db.Column(db.String(3000))
    # position_id = db.Column(db.String(200), nullable=True)
# class Company(db.Model):
#     """User's Bookmarked Companies."""

#     __tablename__ = "Company"

#     company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     company_name = db.Column(db.String(100), nullable=False, unique=True)
#     industry = db.Column(db.String(100))
#     company_website_url = db.Column(db.String(100))

#     def __repr__(self):
#         """Formats the Company when printed"""

#         return "<User company_id=%d company_name=%s industry=%s company_website_url=%s>" % (self.company_id, self.company_name, self.industry, self.company_website_url)


# class Contacts(db.Model):
#     """User's Contacts"""

#     __tablename__ = "Contacts"

#     contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     contact_first_name = db.Column(db.String(100), nullable=False, unique=True)
#     contact_last_name = db.Column(db.String(100), nullable=False, unique=True)
#     contact_email_address = db.Column(db.String(100))
#     contact_company_name = db.Column(db.String(100))
#     contact_phone_number = db.Column(db.String(50))
#     contact_linkedin_profile = db.Column(db.String(100))
#     contact_type = db.Column(db.String(100))





# class Interviews(db.Model):
#     """User's Interviews"""

#     __tablename__ = "Interviews"

#     interview_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     interview_date = db.Column(db.String(50), nullable=False, unique=True)
#     position_summary = db.Column(db.String(300))
#     interview_type = db.Column(db.String(100))
#     interview_status = db.Column(db.Integer)


# class Notes(db.Model):
#     """User's Position Notes."""

#     __tablename__ = "Notes"

#     notes_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     note = db.Column(db.String(3000))








##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thehunt.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
