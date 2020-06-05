from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
import sqlite3
from forms import SearchForm

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///POW_Project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ajaj'

db = SQLAlchemy(app)

import models

def countpows():
    count = models.Prisoner.query.filter().count()
    return count


@app.route('/')
def home():
    count = countpows()
    return render_template("home.html",number=count)

@app.route('/about')
def about():
    count = countpows()
    return render_template("about.html", number=count)

# Return a search result from the form shown on every page (page_title.html)
@app.route('/records', methods=['POST'])
def search():
    form = SearchForm()
    results = models.Prisoner.query.filter(models.Prisoner.surname.ilike('%{}%'.format(form.query.data))).all()
    results1 = results[::3]
    results2 = results[1::3]
    results3 = results[2::3]
    return render_template('results.html', title='Search Results', results=results, val=form.query.data, results1=results1, results2=results2, results3=results3)

@app.route('/browse')
def browse():
    #pows = models.Prisoner.query.all()
    return render_template("browse.html")

@app.route('/pow/<int:val>')
def pow(val):
    pow = models.Prisoner.query.filter_by(id=val).first_or_404()
    surname = pow.surname
    capture = pow.Capture
    count = models.Prisoner.query.filter(models.Prisoner.capture==capture.id).count()
    if capture.date == "Greece":
        inor = "in"
        sent = "at this location"
    elif capture.date == "Crete":
        inor = "in"
        sent = "at this location"
    elif capture.date == "Greece/Crete":
        inor = "in"
        sent = "at this location"
    else:
        inor = "on"
        sent = "on this date"
    return render_template("prisoner.html", val=val, prisoner=pow, page_title=surname, inor=inor, sent=sent, count=count)

@app.route('/results/<val>')
def results(val):
    #will have to add try except for search use
    pows = models.Prisoner.query.filter(models.Prisoner.surname.ilike('{}%'.format(val))).all()
    #For better display of results I split the results over 3 tables. For resizing purposes it also returns all results incase screen size is too small for 3 table display
    pows1 = pows[::3]
    pows2 = pows[1::3]
    pows3 = pows[2::3]
    val = val.upper()
    return render_template("results.html",val=val, results1=pows1, results2=pows2, results3=pows3)

# inject search form (flask-wtf) into all pages
@app.context_processor
def inject_search():
    searchform = SearchForm()
    return dict(searchform=searchform)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)
