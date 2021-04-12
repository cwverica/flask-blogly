"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)

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
    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_new_post_form(user_id):
    '''submits the new post for the user'''

    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    for tag in Tag.query.all():
        if request.form[tag.id]:
            post_tag = PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(post_tag)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    '''shows the form for editing an already existing post'''

    post = Post.query.filter(Post.id == post_id).one()
    tags = Tag.query.all()
    

    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_edit_post_form(post_id):
    '''submits the edited post'''

    post = Post.query.filter(Post.id == post_id).one()
    post.title = request.form['title']
    post.content = request.form['content']

    for tag in Tag.query.all():
        if request.form[tag.id]:
            if not PostTag.query.filter((PostTag.post_id == post.id) & (PostTag.tag_id == tag.id)).one_or_none():
                post_tag = PostTag(post_id=post.id, tag_id=tag.id)
                db.session.add(post_tag)
        else:
            if PostTag.query.filter((PostTag.post_id == post.id) & (PostTag.tag_id == tag.id)).one_or_none():
                PostTag.query.filter((PostTag.post_id == post.id) & (PostTag.tag_id == tag.id)).delete()
            
    
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    '''deletes specified post'''

    Post.query.filter(Post.id==post_id).delete()
    db.session.commit()

    return redirect('/users')


########################################################
# Views for the tags below
########################################################

# GET /tags
# Lists all tags, with links to the tag detail page.
@app.route('/tags')
def show_all_tags():
    '''displays all of the existing tags'''
    tags = Tag.query.all()

    return render_template('all_tags.html', tags=tags)


# GET /tags/[tag-id]
# Show detail about a tag. Have links to edit form and to delete.
@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    '''displays details about specified tag'''
    
    tag = Tag.query.filter(Tag.id == tag_id).one()

    return render_template('tag_details.html', tag=tag)


# GET /tags/new
# Shows a form to add a new tag.
@app.route('/tags/new')
def show_new_tag_form():
    '''displays tag creation form'''
    
    return render_template('new_tag.html')


# POST /tags/new
# Process add form, adds tag, and redirect to tag list.
@app.route('/tags/new', methods=['POST'])
def submit_new_tag_form():
    '''submits a new tag to the db'''

    name = request.form['name']
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


# GET /tags/[tag-id]/edit
# Show edit form for a tag.
@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    '''displays form to edit a tag name'''

    tag = Tag.query.filter(Tag.id == tag_id).one()

    return render_template('edit_tag.html', tag=tag)


# POST /tags/[tag-id]/edit
# Process edit form, edit tag, and redirects to the tags list.
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag_form(tag_id):

    tag = Tag.query.filter(Tag.id == tag_id).one()
    tag.name = request.form['name']

    db.session.commit()
    return redirect('/tags')


# POST /tags/[tag-id]/delete
# Delete a tag.
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''deletes selected tag'''

    Tag.query.filter(Tag.id == tag_id).delete()

    db.session.commit()
    return redirect('/tags')