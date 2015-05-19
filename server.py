"""HB Spring 2015 Final project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Position, User_Assets


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("base.html")


@app.route('/position')
def position_page():
    """Display user's position."""
    return render_template("positions.html")


@app.route('/submit_position', methods=['POST'])
def position_form():
    """Process a user's position."""
    title = request.form["title"]
    position_summary = request.form["position_summary"]
    deadline = request.form["deadline"]
    company_name = request.form["company_name"]
    location = request.form["location"]
    application_status = request.form["status"]
    position_url = request.form["position_url"]

    new_position = Position(title=title, position_summary=position_summary, deadline=deadline, company_name=company_name, location=location, application_status=application_status, position_url=position_url)

    db.session.add(new_position)
    db.session.commit()

    flash("Position %s added!" % title)
    return redirect('/')


@app.route("/listofpositions")
def position_list():
    """Shows list of positions."""
    positions = Position.query.all()
    print positions
    return render_template("position_list.html", positions=positions)


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
