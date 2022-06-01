from upapp.apis.user import *
from upapp.tests.data_creator import BaseTest


class UserTestCase(BaseTest):

    def test_get_user(self):
        user = self.users[0]
        resp = self.makeRequest(f'account-user/{user.id}/', self.REQUEST_GET)
        self.assertEqual(resp.data['id'], user.id)

    def test_job_preferences(self):
        resp = self.makeRequest('user-preferences/', self.REQUEST_PUT, data={

        })