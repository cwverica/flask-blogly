"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "thisismySECRETcode!"
debug = DebugToolbarExtension(app)

@app.route('/')
def home_redirect():
    return redirect('/users')


@app.route('/users')
def show_all_users():
    '''Returns users and lists all'''

    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('all_users.html', users=users)


@app.route('/users/new')
def show_user_form():
    '''shows add user form'''

    return render_template('add_user_form.html')


@app.route('/users/new', methods=['POST'])
def submit_user_form():
    """Add pet and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    '''shows users details, button for edit, button for delete'''

    user = User.query.filter_by(id=user_id).one()

    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    '''shows edit user form'''

    user = User.query.filter_by(id=user_id).one()

    return render_template('edit_form.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit_user_form(user_id):
    '''recieves edited data, updates, redirects to users'''

    user = User.query.filter_by(id=user_id).one()
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.commit()


    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    '''deletes user, redirects to users'''

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')