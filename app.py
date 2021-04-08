"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

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

########################################################
# Views for the users
########################################################

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

########################################################
# Views for the posts below
########################################################

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    '''shows the details of the individual post'''

    post = Post.query.filter(Post.id == post_id).one()
    return render_template('post_details.html', post=post)


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    '''shows the form for submitting a new post for a user'''

    user = User.query.filter(User.id == user_id).first()

    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_new_post_form(user_id):
    '''submits the new post for the user'''

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    '''shows the form for editing an already existing post'''

    post = Post.query.filter(Post.id == post_id).one()

    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_edit_post_form(post_id):
    '''submits the edited post'''

    post = Post.query.filter(Post.id == post_id).one()
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):

    Post.query.filter(Post.id==post_id).delete()
    db.session.commit()

    return redirect('/users')