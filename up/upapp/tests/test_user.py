from upapp.apis.user import *
from upapp.tests.data_creator import BaseTest


class UserTestCase(BaseTest):

    def test_get_user(self):
        user = self.users[0]
        resp = self.makeRequest(f'account-user/{user.id}/', self.REQUEST_GET)
        self.assertEqual(resp.data['id'], user.id)

    def test_job_preferences(self):
        # Preferences
        companySizes = [self.companySizes[0].id, self.companySizes[1].id, self.companySizes[2].id]
        countries = [self.countries[0].id]
        remoteBits = 2
        salary = 150000
        resp = self.makeRequest('user-preferences/', self.REQUEST_PUT, data={
            'companySizes': companySizes,
            'countries': countries,
            'preferenceRemoteBits': remoteBits,
            'salary': salary
        })

        self.assertEqual(resp.status_code, 200)
        preferences = resp.data['preferences']

        self.assertListEqual([p['id'] for p in preferences['companySizes']], companySizes)
        self.assertListEqual([p['id'] for p in preferences['countries']], countries)
        self.assertEqual(preferences['remoteBits'], remoteBits)
        self.assertEqual(preferences['salary'], salary)


class UserJobApplicationTestCase(BaseTest):

    def test_post_job_app(self):
        user = self.users[0]

        # Post as the user creating the application
        resp = self.makeRequest(f'user-job-application/', self.REQUEST_POST, data={
            'employerJobId': self.employerJobs[0].id,
            'userId': user.id,
        })

        # Post as the employer creating the application
