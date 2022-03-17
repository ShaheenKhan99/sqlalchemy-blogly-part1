from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter test with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error infor
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyViewTestCase(TestCase):
    """ Tests view functions for Blogly app"""

    def setUp(self):
        """ Add sample user and post before every test """

        User.query.delete()
        Post.query.delete()

        user = User(first_name="TestUser", last_name="TestLastName", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="TestPost", content="Blogly1234", user_id=self.user_id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id



    def tearDown(self):
        """ Clean up any fouled transaction """

        db.session.rollback()


    def test_home(self):
        """ Check whether homepage is rendered correctly"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Blogly Recent Posts</h1>', html)

############################################################################

# Tests for user view functions

    def test_show_all_users(self):
        """Check if list of all users is displayed """
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)

    
    def test_show_user_form(self):
        """ Check whether new user form is displayed"""
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)


    def test_create_user(self):
        """ Check if user is redirected to all users page after creating account"""
        with app.test_client() as client:
            d = {"first_name": "TestUser2", "last_name":"User2LastName", "image_url": "https://images.unsplash.com/photo-1579935110464-fcd041be62d0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8ZGFydGglMjB2YWRlcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)

    def test_show_user_details(self):
        """ Check whether details of speficic user are displayed"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestUser  TestLastName</h1>', html)  


    def test_show_edit_page(self):
        """ Check if form to edit user details is rendered"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)


    def test_update_user_details(self):
        """ Check if user is redirected to all users page after editing user details """
        with app.test_client() as client:
            d = {"first_name": "TestUser3", "last_name":"User3LastName", "image_url": "https://images.unsplash.com/photo-1579935110464-fcd041be62d0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8ZGFydGglMjB2YWRlcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)


    def test_delete_user(self):
        """ Check if user is redirected to all users page after deleting account"""
        with app.test_client() as client:
            d = {"first_name": "TestUser4", "last_name":"User4LastName", "image_url": "https://images.unsplash.com/photo-1579935110464-fcd041be62d0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8N3x8ZGFydGglMjB2YWRlcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60"}
            resp = client.post(f"/users/{self.user_id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)

###########################################################################

# Tests for posts view functions
    
    def test_show_post_form(self):
        """ Check if form for adding post for specific user is rendered"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add Post for TestUser TestLastName</h1>', html)
    

    def test_create_post(self):
        """ Check if user is redirected to user details page after creatign post """
        with app.test_client() as client:
            d = {"title": "Test2Post", "content": "Just Posting", "user_id": "{self.user_id}"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestUser  TestLastName</h1>', html)


    def test_show_post(self):
        """ Check if new post is displayed on the post details page"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestPost</h1>', html) 


    def test_show_post_edit_form(self):
        """ Check if form to edit post is rendered"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit Post</h1>', html)


    def test_update_post(self):
        """CHeck if user is redirected to post details page after editing the post"""
        with app.test_client() as client:
            d = {"title": "Test3Post", "content": "Just Another Posting", "user_id": "{self.user_id}"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test3Post</h1>', html)

    def test_delete_post(self):
        """ Check id user is redirected to all users page after deleting post"""
        with app.test_client() as client:
            d = {"title": "Test3Post", "content": "Just Another Posting", "user_id": "{self.user_id}"}
            resp = client.post(f"/posts/{self.post_id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestUser  TestLastName</h1>', html)