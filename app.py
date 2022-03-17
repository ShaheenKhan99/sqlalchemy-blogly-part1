"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

# Post routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_post_form(user_id):
    """ Show form to create new post """

    user = User.query.get_or_404(user_id)
    return render_template('posts/newpost.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """ Handle form submission for new post by specific user"""

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user=user)

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
    return render_template('posts/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle form submission for editing specific post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

 
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








