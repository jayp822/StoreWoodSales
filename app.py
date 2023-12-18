from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# CREATE DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wood.db"

# CREATE THE EXTENSION
db = SQLAlchemy()

# initialize the app with the extension
db.init_app(app)

today = datetime.date.today()
now = datetime.datetime.now()
year = now.year


# CREATE TABLE

class Wood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), unique=False, nullable=False)
    time = db.Column(db.String(20), unique=True, nullable=False)
    employee = db.Column(db.String(20), unique=False, nullable=False)
    amount = db.Column(db.Float, unique=False, nullable=False)


with app.app_context():
    db.create_all()

# Initialize Database
# with app.app_context():
#     new_sale = Wood(id=1, date=today.strftime("%b-%d-%Y"), time=now.strftime("%H:%M:%S"), employee="Jay Patel", amount=10.00)
#     db.session.add(new_sale)
#     db.session.commit()

@app.route('/')
def home():
    result = db.session.query(Wood).all()
    return render_template('index.html', sales=result, year=year)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_sale = Wood(
            date=today.strftime("%b-%d-%Y"),
            time=now.strftime("%H:%M:%S"),
            employee=request.form["employee"],
            amount=request.form["amount"]
        )
        db.session.add(new_sale)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', year=year)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        wood_id = request.form["id"]
        wood_to_update = db.get_or_404(Wood, wood_id)
        wood_to_update.employee = request.form["employee"]
        wood_to_update.amount = request.form["amount"]
        db.session.commit()
        return redirect(url_for('home'))
    wood_id = request.args.get('id')
    wood_selected = db.get_or_404(Wood, wood_id)
    return render_template("edit.html", wood=wood_selected, year=year)


@app.route("/delete")
def delete():
    wood_id = request.args.get('id')

    # DELETE RECORD BY ID

    wood_to_delete = db.get_or_404(Wood, wood_id)
    db.session.delete(wood_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
