from __future__ import absolute_import

from sentry.testutils import AcceptanceTestCase
from sentry.models import Project


class CreateProjectTest(AcceptanceTestCase):
    def setUp(self):
        super(CreateProjectTest, self).setUp()
        self.user = self.create_user('foo@example.com')
        self.org = self.create_organization(
            name='Rowdy Tiger',
        )
        self.login_as(self.user)

        self.path = '/organizations/{}/projects/new/'.format(self.org.slug)

    def test_simple(self):
        self.team = self.create_team(organization=self.org, name='Mariachi Band')
        self.create_member(
            user=self.user,
            organization=self.org,
            role='owner',
            teams=[self.team],
        )
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')

        self.browser.click('.platformicon-java')
        self.browser.snapshot(name='create project')

        self.browser.click('.new-project-submit')
        self.browser.wait_until(title='Mariachi Band / Java')

        project = Project.objects.get(organization=self.org)
        assert project.name == 'Java'
        assert project.platform == 'java'
        assert project.team_id == self.team.id
        self.browser.snapshot(name='docs redirect')

    def test_no_teams(self):
        self.create_member(
            user=self.user,
            organization=self.org,
            role='owner',
            teams=[],
        )
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')
        self.browser.snapshot(name='create project no teams')

    def test_many_teams(self):
        self.team = self.create_team(organization=self.org, name='Mariachi Band')
        self.team2 = self.create_team(organization=self.org, name='team two')
        self.create_member(
            user=self.user,
            organization=self.org,
            role='owner',
            teams=[self.team, self.team2],
        )
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')
        self.browser.snapshot(name='create project many teams')
