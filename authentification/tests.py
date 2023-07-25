from django.test import TestCase, Client

class LoginPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalid_credentials(self):
        response = self.client.post('user/login', {'username': 'invalid_username', 'password': 'invalid_password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login credentials. Please try again.')


