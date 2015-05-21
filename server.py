"""HB Spring 2015 Final project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Position, User_Assets, Notes


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    return render_template("welcomepage.html")


@app.route('/dashboard')
def dashboard():
    """Dashboard."""
    positions = Position.query.all()
    documents = User_Assets.query.all()
    notes = Notes.query.all()
    users = User.query.all()
    # user = User.query.all()
    return render_template("dashboard.html", users=users, positions=positions, documents=documents, notes=notes)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/submit_register', methods=['POST'])
def register_process():
    """Process registration."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    password = request.form["password"]
    picture = request.form["picture"]
    email_address = request.form["email_address"]
    last_login = "Login"
    user_LinkedIn_url = request.form["linkedin_url"]
    user_Twitter_url = request.form["twitter_url"]
    user_Facebook_url = request.form["facebook_url"]
    user_website_url = request.form["website_url"]

    new_user = User(first_name=first_name, last_name=last_name, last_login=last_login, password=password, picture=picture, email_address=email_address, user_LinkedIn_url=user_LinkedIn_url, user_Twitter_url=user_Twitter_url, user_Facebook_url=user_Facebook_url, user_website_url=user_website_url)

    db.session.add(new_user)
    db.session.commit()

    #query for new user and add to flask sesssion, two seperate things  

    flash("Thanks %s for joining the hunt!" % first_name)
    return redirect("/dashboard")
  


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email_address = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email_address=email_address).first()

    if not user:
        flash("No such user")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out. Thanks for using The Hunt!")
    return redirect("/")

# @app.route('/user')
# def user_page():
#     """This page will display a user's details."""
#     return render_template("user_detail.html")


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
    #I need to add code here that prompts a user to upload new positions
    #if there are no positions listed

    positions = Position.query.all()
    print positions
    return render_template("position_list.html", positions=positions)


@app.route("/position/<int:position_id>")
def position(position_id):
    """Shows info about a position."""
    position = Position.query.get(position_id)
    print position
    return render_template("position.html", position=position)


@app.route('/documents')
def documents_page():
    """This will show the a page for an user's positions."""
    return render_template("documents.html")


@app.route('/submit_documents', methods=['POST'])
def document_form():
    """Process a user's documents."""
    asset_type = request.form["document_type"]
    asset_content = request.form["document"]

    new_document = User_Assets(asset_type=asset_type, asset_content=asset_content)

    db.session.add(new_document)
    db.session.commit()

    flash("Your %s has been added!" % asset_type)
    return redirect('/')


@app.route("/listofdocuments")
def document_list():
    """Shows list of documents."""
    documents = User_Assets.query.all()
    print documents
    return render_template("document_list.html", documents=documents)


@app.route("/document/<int:user_asset_id>")
def document(user_asset_id):
    """Shows info about a position."""
    document = User_Assets.query.get(user_asset_id)
    print document
    return render_template("document.html", document=document)


@app.route('/notes')
def notes_page():
    """This will show the a page for an user's positions."""
    return render_template("notes.html")


@app.route('/submit_notes', methods=['POST'])
def note_form():
    """Process a user's notes."""
    note_type = request.form["note_type"]
    note_details = request.form["note_details"]

    new_note = Notes(note_type=note_type, note_details=note_details)

    db.session.add(new_note)
    db.session.commit()

    flash("Your %s has been added!" % note_type)
    return redirect('/')


@app.route("/listofnotes")
def note_list():
    """Shows list of notes."""
    notes = Notes.query.all()
    print notes
    return render_template("note_list.html", notes=notes)


@app.route("/notes/<int:note_id>")
def note(note_id):
    """Shows info about a note."""
    note = Notes.query.get(note_id)
    print note
    return render_template("note.html", note=note)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
