from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()


class UserViewsTestCase(TestCase):
    """Testing the routes for the app"""

    def setUp(self):
        db.create_all()
        User.query.delete()
        Post.query.delete()

        user = User(first_name="Jacob", last_name="Radford", img_url="https://media.gettyimages.com/photos/portrait-teenager-picture-id846730696?s=2048x2048")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title="PostTitle", content="PostContent", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def test_list_all_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)  

            self.assertIn("Jacob", html)
            self.assertEqual(resp.status_code, 200)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertIn("Jacob", html)
            self.assertIn("Delete", html)
            self.assertIn("Edit", html)
            self.assertEqual(resp.status_code, 200)

    def test_add_new_user(self):
        with app.test_client() as client:
            data = {'first_name': 'Jenny', 'last_name': 'Porter', 'img_url': 'https://media.gettyimages.com/photos/stay-hungry-for-success-picture-id1040964880?s=2048x2048' }
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Jenny", html)
            self.assertIn("Porter", html)
            self.assertIn("Jacob", html)
            self.assertEqual(resp.status_code, 200)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {'first_name': 'Jenny', 'last_name': 'Porter', 'img_url': 'https://media.gettyimages.com/photos/stay-hungry-for-success-picture-id1040964880?s=2048x2048' }
            resp = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("Jenny", html)
            self.assertIn("Porter", html)
            self.assertNotIn("Jacob", html)
            self.assertEqual(resp.status_code, 200)

    def test_show_post_details(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertIn("PostTitle", html)
            self.assertIn("PostContent", html)
            self.assertEqual(resp.status_code, 200)

    def test_add_new_post(self):
        with app.test_client() as client:
            data = {'title': 'NewestTitle', 'content': 'NewestContent', 'user_id':self.user_id}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("NewestTitle", html)
            self.assertIn("PostTitle", html)
            self.assertIn("Jacob", html)
            self.assertEqual(200, resp.status_code)

    def test_edit_post(self):
        with app.test_client() as client:
            data = {'title': 'NewestTitle', 'content': 'NewestContent', 'user_id':self.user_id}
            resp = client.post(f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn("NewestTitle", html)
            self.assertNotIn("PostTitle", html)
            self.assertIn("Jacob", html)
            self.assertEqual(200, resp.status_code)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            resp2 = client.get(f'/users/{self.user_id}')
            html2 = resp2.get_data(as_text=True)

            self.assertIn("Jacob", html2)
            self.assertNotIn("PostTitle", html2)
            self.assertEqual(200, resp.status_code)
            self.assertEqual(200, resp2.status_code)

