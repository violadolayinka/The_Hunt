"""HB Spring 2015 Final project."""

from jinja2 import StrictUndefined
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Position, Documents, Notes


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
#if the user's email already exists on file
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


# @app.route('/login')
# def login_form():
#     """Show login form."""
#     return render_template("login_form.html")


# @app.route('/login', methods=['POST'])
# def login_process():
#     """Process login."""
#     email_address = request.form.get("email")
#     password = request.form.get("password")

#     user = User.query.filter_by(email_address=email_address).first()

#     if not user:
#         flash("Please try again!")
#         return redirect('/login')

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect('/login')

#     session["user_id"] = user.user_id

#     flash("Logged in")
#     return redirect('/dashboard')


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
    # FIXME check for logged in user like in above
    # if "user_id" in session:
    #     my_user_id = session["user_id"]
    #     user_id = User.query.filter_by(user_id=my_user_id).one()

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

    flash("Position: %s  added!" % title)
    return redirect("/listofpositions")

# else:
#     flash("Please log into  The Hunt!")
#     return redirect('/')


@app.route("/delete_position/<int:position_id>", methods=["GET", "POST"])
def delete_position(position_id):
    """Deletes a user's position."""
    if "user_id" in session:
        position = Position.query.filter_by(position_id=position_id).one()
        print position
        if request.method == 'POST':
            Position.query.filter_by(position_id=position_id).delete()
            db.session.commit()
            flash("Position: %s  has been deleted!" % position.title)
            return redirect('/dashboard')
    else:
        flash("Please log into  The Hunt!")
        return redirect('/')

# @app.route('/delete_position')
# def delete_position():
#     """This route deletes a position."""
#     del session["user_id"]

#     flash("Logged Out. Thanks for using The Hunt!")
#     return redirect("/")


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
    #FIXME maybe, make sure the user owns these positions
    if "user_id" in session:
        position = Position.query.filter_by(position_id=position_id).one()
        print "Here's the user currently in session"
        # print "This is the userID", user.user_id
        print "This is the position userid", position.user_id

        if session['user_id'] != position.user_id:
            flash("Whoops! You may have accessed the wrong page!")
            return redirect('/dashboard')

        notes = Notes.query.filter_by(position_id=position_id).all()
        document = Documents.query.filter_by(position_id=position_id).all()

        if request.method == "POST":
            new_application_status = request.form["status"]
            position.application_status = new_application_status
            db.session.commit()
            flash("Your application status is updated!")

        return render_template("position.html", user_id=session['user_id'], position=position, notes=notes, document=document)
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

    # if "user_id" in session:
    #     u = session["user_id"]
    #     #TODO check if we use user_id?
    #     return render_template("documents.html", user_id=u)
    # else:
    #     flash("Please log into  The Hunt!")
    #     return redirect('/')


@app.route('/submit_documents', methods=['POST'])
def document_form():
    """Process a user's documents."""
    # FIXME
    position_id = request.form["position_id"]
    document_type = request.form["document_type"]
    #TODO see if they have a note or a new document, make sure you dont add empty attributes/get key errors
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
        #FIXME
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
    #FIXME check for login
    """Shows info about a position."""

    document = Documents.query.get(document_id)
    return render_template("document.html", document=document)


@app.route("/listofnotes")
def note_list():
    """Shows list of notes."""
    # if "user_id" in session:
    #     my_user_id = session["user_id"]
    #     user = User.query.filter_by(user_id=my_user_id).one()
    #     positions = Position.query.filter_by(user_id=my_user_id).all()
    #     return render_template("dashboard.html", user=user, positions=positions)
    # else:
    #     flash("Please log into  The Hunt!")
    #     return redirect('/')

    #FIXME check for login
    u_id = session["user_id"]
    print u_id
    print type(u_id)
    position_object = Position.query.get(u_id)
    pos_id = position_object.position_id
    notes = Notes.query.filter_by(position_id=pos_id).all()

    return render_template("note_list.html", notes=notes)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
