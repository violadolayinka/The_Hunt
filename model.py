"""Models and database functions for HB Spring 2015 Final project."""


from flask_sqlalchemy import SQLAlchemy

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
    last_login = db.Column(db.String(60))
    user_LinkedIn_url = db.Column(db.String(100))
    user_Twitter_url = db.Column(db.String(100))
    user_Facebook_url = db.Column(db.String(100))
    user_website_url = db.Column(db.String(100))
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'))

    position = db.relationship("Position", backref=db.backref("user", order_by=user_id))

    def __repr__(self):
        """I'm adding this statement to make sure that my relationship is established"""
        return "<User user_id=%s first_name=%d position_id=%s>" % (self.user_id, self.first_name, self.position_id)


class Position(db.Model):
    """User's Positions"""

    __tablename__ = "position"

    position_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50))
    position_summary = db.Column(db.String(300))
    deadline = db.Column(db.String(60))
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    application_status = db.Column(db.String(50))
    position_url = db.Column(db.String(100))
    user_asset_id = db.Column(db.Integer, db.ForeignKey('user_assets.user_asset_id'))

    user_assets = db.relationship("User_Assets", backref=db.backref("position", order_by=position_id))

    def __repr__(self):
        """I'm adding this statement to make sure that my relationship is established"""
        return "<Position position_id=%s title=%s user_asset_id=%s>" % (self.position_id, self.title, self.user_asset_id)


class User_Assets(db.Model):
    """User's Job Applicaton Assets."""

    __tablename__ = "user_assets"

    user_asset_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    asset_type = db.Column(db.String(100))
    asset_content = db.Column(db.String(3000))


class Notes(db.Model):
    """User's Notes."""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    note_type = db.Column(db.String(3000))
    note_details = db.Column(db.String(3000))
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'))
    user_asset_id = db.Column(db.Integer, db.ForeignKey('user_assets.user_asset_id'))

    position_note = db.relationship("Position", backref=db.backref("notes", order_by=note_id))
    # user_assets_ = db.relationship("User_Assets", backref=db.backref("position", order_by=position_id))

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
