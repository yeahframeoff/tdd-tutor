from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        try:
            user.full_clean()
        except ValidationError as e:
            self.fail("User with email only is not valid. %s" % e.message_dict)

    def test_email_is_primary_key(self):
        user = User()
        self.assertFalse(hasattr(user, 'id'))

    def test_is_authenticated(self):
        user = User()
        self.assertTrue(user.is_authenticated())
