"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'itsasecret'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
  """Show home page"""
  posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
  return render_template('posts/homepage.html', posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """ Show 404 NOT FOUND page"""

    return render_template('404.html', 404)


###########################################################################

# User routes

@app.route('/users')
def show_all_users():
    """Show list of all users in database"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def show_user_form():
    """Show form to create new user"""
    return render_template('users/new.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """ Handle form submission for new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name,        image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show details about  specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """ Show edit form for specific user"""
    
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user_details(user_id):
    """Handle form submission for updating user details for specific user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} updated.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect('/users')

###########################################################################

# Posts routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_post_form(user_id):
    """ Show form to create new post """

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/newpost.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """ Handle form submission for new post by specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post titled '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>', methods=["GET"])
def show_post(post_id):
    """ Show a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit_form(post_id):
    """Show form to edit specific post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle form submission for editing specific post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
 
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' updated.")

    return redirect(f"/posts/{post_id}")   


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Delete specific post """

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f"/users/{post.user_id}")

#################################################################

# Tags routes

@app.route('/tags')
def show_all_tags():
    """Show list of all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/<int:tag_id>', methods=["GET"])
def show_tag(tag_id):
    """ Show a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_details.html', tag=tag)


@app.route('/tags/new', methods=["GET"])
def show_create_tag_form():
    """Display form to create new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def create_tag():
    """ Handle form submission for creating new tag"""

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    name = request.form['name']

    new_tag = Tag(name=name, posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash(f"New tag '{new_tag.name}' added.")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag_form(tag_id):
    """ Display form to edit tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Handle form submission for editing tag """

    tag = Tag.query.get_or_404(tag_id)
    tag.name= request.form['name']

    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag name has been updated to '{tag.name}' ")

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle form submission for deleting tag """

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag named '{tag.name}' deleted.")

    return redirect('/tags')