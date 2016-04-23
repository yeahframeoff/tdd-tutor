from django.conf import settings

from .base import FunctionalTest
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY

User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest
        self.browser.get(self.server_url + '/404_nonexisting_page/')
        self.browser.add_cookie({
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'path': '/',
        })

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'yeahframeoff@yeahframeoff.com'

        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email=email)

        # Make me a logged in user
        self.create_pre_authenticated_session(email=email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email=email)
