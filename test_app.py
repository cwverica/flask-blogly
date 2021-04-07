from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Testing the routes for the app"""

    def setUp(self):
        User.query.delete()

        user = User(first_name="Jacob", last_name="Radford", img_url="https://media.gettyimages.com/photos/portrait-teenager-picture-id846730696?s=2048x2048")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

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
