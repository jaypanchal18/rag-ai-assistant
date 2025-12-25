import unittest
from app import create_app, db
from app.models import User, Post
from flask import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='newuser', email='new@example.com')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_user_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_create_post(self):
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        response = self.client.post('/posts', data={
            'title': 'Test Post',
            'content': 'This is a test post.'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Test Post', response.data)

    def test_get_posts(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_invalid_route(self):
        response = self.client.get('/invalid-route')
        self.assertEqual(response.status_code, 404)

    def test_post_deletion(self):
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        post = Post(title='Post to delete', content='Content to delete', author=self.user)
        db.session.add(post)
        db.session.commit()
        response = self.client.delete(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Post.query.get(post.id))

if __name__ == '__main__':
    unittest.main()