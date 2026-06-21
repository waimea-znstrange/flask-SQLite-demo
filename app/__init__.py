#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")


#-----------------------------------------------------------
# New creature form
#-----------------------------------------------------------
@app.get("/creature/new")
def show_creature_form():
    return render_template("pages/creature_form.jinja")


#-----------------------------------------------------------
# Handle the creature form
#-----------------------------------------------------------
@app.post("/creature/new")
def process_creature_form():
    # Get the form data
    species = request.form.get("species", "unknown").strip()
    name = request.form.get("name", "unknown").strip()
    # Connect to the DB
    with connect_db() as db:

        sql = """
            INSERT INTO creatures (species, name)
            VALUES (?, ?)
        """

        params = (species, name)

        # Run the query
        db.execute(sql, params)

        flash(f"Creature {name} added successfully")
        # We're done so back to the list
        return redirect("/creatures")



#-----------------------------------------------------------
# Creature deletion - Delete a creature via ID
#-----------------------------------------------------------
@app.get("/creature/<int:id>/delete")
def delete_a_creature(id):
    with connect_db() as db:
        sql = """
            DELETE FROM creatures
            WHERE id=?
        """
        params = (id,)
        db.execute(sql, params)

        # Back to the list
        flash("Creature deleted", "success")
        return redirect("/creatures")


#-----------------------------------------------------------
# Creature list page - Show all the creatures
#-----------------------------------------------------------
@app.get("/creatures")
def show_all_creatures():
    with connect_db() as db:
        sql = """
            SELECT id, species, name
            FROM creatures
        """
        params = ()
        creatures = db.execute(sql, params).fetchall()

        return render_template("pages/creature_list.jinja", creatures=creatures)


#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

