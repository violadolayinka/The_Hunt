"""HB Spring 2015 Final project."""

from jinja2 import StrictUndefined
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Position, Documents, Notes, Contact


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    return render_template("welcomepage.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""
    email_address = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email_address=email_address).first()

    if not user:
        flash("Please try again!")
        return redirect('/')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/')

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    """Dashboard."""
    if "user_id" in session:
        my_user_id = session["user_id"]
        user = User.query.filter_by(user_id=my_user_id).one()
        positions = Position.query.filter_by(user_id=my_user_id).all()
        return render_template("dashboard.html", user=user, positions=positions)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route('/register')
def registration():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/submit_register', methods=['POST'])
def process_registration():
    """Adds a new user to the database"""
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    picture = request.form.get("picture")
    email_address = request.form.get("email_address")
    linkedin_url = request.form.get("linkedin_url")
    twitter_url = request.form.get("twitter_url")
    facebook_url = request.form.get("facebook_url")
    website_url = request.form.get("website_url")
    preexisting_user = User.query.filter_by(email_address=email_address).first()
    if preexisting_user:
        flash("This email address is already on file. Please log in!")
        return redirect('/')

    new_user = User(first_name=first_name, last_name=last_name, password=password,
                    picture=picture, email_address=email_address, linkedin_url=linkedin_url,
                    twitter_url=twitter_url, facebook_url=facebook_url,
                    website_url=website_url)

    db.session.add(new_user)
    db.session.commit()

    flash("Thanks %s for joining the hunt!" % first_name)
    return redirect('/')


@app.route('/logout')
def logout():
    """Log out."""
    del session["user_id"]

    flash("Logged Out. Thanks for using The Hunt!")
    return redirect("/")


@app.route('/position')
def position_page():
    """Display user's position."""
    if "user_id" in session:
        my_user_id = session["user_id"]
        user = User.query.filter_by(user_id=my_user_id).one()
        positions = Position.query.filter_by(user_id=my_user_id).all()
        return render_template("positions.html", user=user, positions=positions)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route('/submit_position', methods=['POST'])
def position_form():
    """Process a user's position."""
    u = session["user_id"]
    title = request.form["title"]
    position_summary = request.form["position_summary"]
    deadline = request.form["deadline"]
    company_name = request.form["company_name"]
    location = request.form["location"]
    application_status = request.form["status"]
    position_url = request.form["position_url"]

    new_deadline = datetime.strptime(deadline, "%Y-%m-%d")

    new_position = Position(user_id=u, title=title, position_summary=position_summary,
                            deadline=new_deadline, company_name=company_name,
                            location=location, application_status=application_status,
                            position_url=position_url)

    db.session.add(new_position)
    db.session.commit()

    contact_name = request.form["contact_name"]
    contact_email_address = request.form["email_address"]
    contact_phone_number = request.form["phone_number"]
    position_id = new_position.position_id

    new_contact = Contact(name=contact_name, email_address=contact_email_address,
                          phone_number=contact_phone_number, position_id=position_id)
    db.session.add(new_contact)
    db.session.commit()

    flash("Position: %s  added!" % title)
    return redirect("/listofpositions")


@app.route("/delete_position/<int:position_id>", methods=["GET", "POST"])
def delete_position(position_id):
    """Deletes a user's position."""
    if "user_id" in session:
        position = Position.query.filter_by(position_id=position_id).one()

        if request.method == 'POST':
            Position.query.filter_by(position_id=position_id).delete()
            db.session.commit()
            flash("Position: %s  has been deleted!" % position.title)
            return redirect('/dashboard')
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route("/listofpositions")
def position_list():
    """Shows list of positions."""
    if "user_id" in session:
        u = session["user_id"]
        positions = Position.query.filter_by(user_id=u).all()
        return render_template("position_list.html", positions=positions)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route("/position/<int:position_id>", methods=["GET", "POST"])
def position(position_id):
    """Shows info about a position."""
    if "user_id" in session:
        position = Position.query.filter_by(position_id=position_id).one()
        # positions = Position.query.filter_by(user_id=session['user_id']).one()
        print "Here's the user currently in session"
        print "This is the position userid", position.user_id

        if session['user_id'] != position.user_id:
            flash("Whoops! You may have accessed the wrong page!")
            return redirect('/dashboard')

        notes = Notes.query.filter_by(position_id=position_id).all()
        document = Documents.query.filter_by(position_id=position_id).all()
        contacts = Contact.query.filter_by(position_id=position_id).all()

        if request.method == "POST":
            new_application_status = request.form["status"]
            position.application_status = new_application_status
            db.session.commit()
            flash("Your application status is updated!")

        return render_template("position.html", user_id=session['user_id'], position=position, notes=notes, document=document, contacts=contacts)
    else:

        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route('/documents')
def documents_page():
    """This will show the a page for an user's documents."""
    if "user_id" in session:
        positions = Position.query.filter_by(user_id=my_user_id).all()
        return render_template("documents.html", user=session['user_id'], positions=positions)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route('/submit_documents', methods=['POST'])
def document_form():
    """Process a user's documents."""
    position_id = request.form["position_id"]
    document_type = request.form["document_type"]
    document_content = request.form["document"]
    note_details = request.form["note_details"]

    new_document = Documents(position_id=position_id, document_type=document_type,
                             document_content=document_content)
    new_note = Notes(position_id=position_id, note_details=note_details)
    db.session.add(new_document)
    db.session.add(new_note)
    db.session.commit()

    flash("Your %s has been added!" % document_type)
    return redirect('/dashboard')


@app.route("/listofdocuments")
def document_list():
    """Shows list of documents."""
    if "user_id" in session:
        u_id = session["user_id"]
        user_object = User.query.get(u_id)
        position = Position.query.get(u_id)

        documents = []

        for position in user_object.positions:
            documents.extend(position.documents)
        return render_template("document_list.html", documents=documents, position=position)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route("/document/<int:document_id>")
def document(document_id):
    """Shows info about a position."""

    document = Documents.query.get(document_id)
    return render_template("document.html", document=document)


@app.route("/listofnotes")
def note_list():
    """Shows list of notes."""
    if "user_id" in session:
        u_id = session["user_id"]
        user_object = User.query.get(u_id)
        print user_object
        note = Notes.query.get(u_id)
        print "Here's the notes:"
        print note
        notes = []

        for note in notes:
            notes.extend(position.notes)
        return render_template("note_list.html", notes=notes, note=note)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route('/contacts')
def contacts_page():
    """This will show the a page for an user's contacts."""
    if "user_id" in session:
        positions = Position.query.filter_by(user_id=my_user_id).all()
        return render_template("contacts.html", user=session['user_id'], positions=positions)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


@app.route("/listofcontacts")
def contacts_list():
    """Shows list of contacts."""
    if "user_id" in session:
        u_id = session["user_id"]
        user_object = User.query.get(u_id)

        contacts = []

        for position in user_object.positions:
            contacts.extend(position.contacts)
        return render_template("contact_list.html", contacts=contacts)
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
