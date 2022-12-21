from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

app.config['SECRET_KEY'] = "bigwhitepotato"
db = SQLAlchemy(app)

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

#MODEL
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a String
    def __repr__(self):
        return '<Name> %r>' % self.name
    
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}</h1>'.format(name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit:
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template('name.html', name=name, form=form)

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, users=users) 

if __name__ == '__main__':
    app.run(host='localhost', debug=True)



