"""Models and database functions for HB Spring 2015 Final project."""


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """User"""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(64), nullable=True)
    picture = db.Column(db.String(100))
    email_address = db.Column(db.String(100))
    user_LinkedIn_url = db.Column(db.String(100))
    user_Twitter_url = db.Column(db.String(100))
    user_Facebook_url = db.Column(db.String(100))
    user_website_url = db.Column(db.String(100))

    def __repr__(self):
        """This will provide helpful information when printed."""
        return "<User user_id=%s first_name=%s>" % (self.user_id, self.first_name)


class Position(db.Model):
    """User's Positions"""

    __tablename__ = "positions"

    position_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))
    note_id = db.Column(db.Integer, db.ForeignKey('notes.note_id'))
    title = db.Column(db.String(50))
    position_summary = db.Column(db.String(300))
    deadline = db.Column(db.DateTime)
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    application_status = db.Column(db.String(50))
    position_url = db.Column(db.String(100))

    document = db.relationship("Documents", backref=db.backref("positions", order_by=position_id))

    note = db.relationship("Notes", backref=db.backref("positions", order_by=position_id))

    def __repr__(self):
        """Provide helpful representation when printed."""
        deadline = self.deadline.strftime("%m/%d/%Y")
        return "<Positions position_id=%s title=%s document_id=%s note_id=%s deadline=%s>" % (self.position_id, self.title, self.document_id, self.note_id, deadline)


class Documents(db.Model):
    """User's Job Applicaton Documents."""

    __tablename__ = "documents"

    document_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    document_type = db.Column(db.String(100))
    document_content = db.Column(db.String(3000))


class Notes(db.Model):
    """User's Notes."""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note_type = db.Column(db.String(3000))
    note_details = db.Column(db.String(3000))
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
