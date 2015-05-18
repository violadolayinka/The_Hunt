"""HB Spring 2015 Final project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import flask.views

from model import connect_to_db, db, User, Position, User_Assets


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("base.html")


@app.route('/user', methods=['GET'])
def user_page():
    """This will show the a page for an user's positions."""

    return render_template("user.html")


@app.route('/position')
def position_page():
    """Process a user's position."""

    # request.form["title"] == "title"
    # request.form["position_summary"] == "position_summary"
    # # deadline = int(request.form["deadline"])
    # request.form["company_name"] == "company_name"
    # request.form["location"] == "location"
    # request.form["status"] == "not_yet_started", "in_progress", "complete", "rejected"
    # request.form["position_url"] == "position_url"

    # # new_position = Position(title=title, position_summary=position_summary, company_name=company_name, location=location, application_status=application_status, position_ur=position_url)

    # # db.session.add(new_position)
    # # db.session.commit()

    return render_template("positions.html")


# class View(flask.views.MethodView):
#     def get(self):
#         """Enable user to provide us with input"""
#         return self._default_actions()

#     def post(self):
#         """Map user input to our program's inputs - display errors if required"""
#         position_summary = flask.request.form["position_summary"]
#         # Alternately, if `result` is not *required*
#         # result = flask.request.form.get("result")
#         return self._default_actions(position_summary=position_summary)

#     def _default_actions(self, result=None):
#         """Deal with the meat of the matter, taking in whatever params we need
#         to get or process our information"""
#         if result is None:
#             return flask.render_template(positions.html)
#         else:
#             return flask.render_template("positions.html", position_summary="position_summary")

# app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])


@app.route('/documents')
def documents_page():
    """This will show the a page for an user's positions."""

    return render_template("documents.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
