import unittest
from app import app, create_app, db
from app.users.models import User
from werkzeug.security import generate_password_hash

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="test_conf")
        self.app.config['WTF_CSRF_ENABLED'] = False  # Вимкнення CSRF для тестів
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_page_loads(self):
        """
        Перевірка завантаження сторінки входу.
        """
        response = self.client.get('/user/login')  # Замініть на правильний маршрут
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_user_login_success(self):
        """
        Перевірка успішного входу користувача.
        """
        with self.app.app_context():
            # Створення користувача
            user = User(username='testuser', email='testuser@example.com')
            user.password = generate_password_hash('testpassword')
            db.session.add(user)
            db.session.commit()

        # Спроба входу
        response = self.client.post('/user/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)

    def test_user_login_failure(self):
        """
        Перевірка невдалої спроби входу (невірний пароль).
        """
        with self.app.app_context():
            # Створення користувача
            user = User(username='testuser', email='testuser@example.com')
            user.password = generate_password_hash('testpassword')
            db.session.add(user)
            db.session.commit()

        # Спроба входу з неправильним паролем
        response = self.client.post('/user/login', data={
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_user_logout(self):
        """
        Перевірка успішного виходу користувача.
        """
        with self.app.app_context():
            # Створення користувача
            user = User(username='testuser', email='testuser@example.com')
            user.password = generate_password_hash('testpassword')
            db.session.add(user)
            db.session.commit()

        # Логін користувача
        self.client.post('/user/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })

        # Вихід із системи
        response = self.client.get('/user/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)


if __name__ == "__main__":
    unittest.main()
