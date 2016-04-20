from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from unittest.mock import patch
User = get_user_model()


@patch('accounts.views.authenticate')
class LoginViewTest(TestCase):
    
    def test_calls_authenticate_with_assertion_from_post(
            self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_once_with(assertion='assert this')


    def test_returns_OK_when_the_user_is_found(
            self, mock_authenticate
    ):
        user = User.objects.create(email="a@b.com")
        user.backend = ''
        mock_authenticate.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'abcdefg'})
        self.assertEqual(response.content.decode(), 'OK')


    def test_gets_logged_in_session_if_authenticate_returns_a_user(
            self, mock_authenticate
    ):
        user = User.objects.create(email="a@b.com")
        user.backend = ''
        mock_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'abcdefg'})
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))


    def test_does_not_get_logged_in_if_authenticate_returns_None(
            self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'abcfedg'})
        self.assertNotIn(SESSION_KEY, self.client.session)
