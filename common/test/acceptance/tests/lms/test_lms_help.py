"""
Test Help links in LMS
"""
import json

from common.test.acceptance.tests.studio.base_studio_test import ContainerBase
from common.test.acceptance.pages.lms.instructor_dashboard import InstructorDashboardPage
from common.test.acceptance.fixtures import LMS_BASE_URL


class TestCohortHelp(ContainerBase):
    """
    Tests help links in Cohort page
    """
    def setUp(self, is_staff=True):
        super(TestCohortHelp, self).setUp(is_staff=is_staff)
        self.enable_cohorting(self.course_fixture)
        self.instructor_dashboard_page = InstructorDashboardPage(self.browser, self.course_id)
        self.instructor_dashboard_page.visit()
        self.cohort_management = self.instructor_dashboard_page.select_cohort_management()

    def get_url_with_changed_domain(self, url):
        """
        Replaces .org with .io in the url
        Arguments:
            url (str): The url to perform replace operation on.
        Returns:
        str: The updated url
        """
        return url.replace('.org/', '.io/')

    def assert_link(self, expected_link, actual_link):
        """
        Assert that 'href' and text inside help DOM element are correct.

        Arguments:
            expected_link (dict): The expected link attributes.
            actual_link (dict): The actual link attribute on page.
        """
        self.assertEqual(expected_link['href'], actual_link.get_attribute('href'))
        self.assertEqual(expected_link['text'], actual_link.text)

    def assert_opened_help_link_is_correct(self, url):
        """
        Asserts that url of browser when help link is clicked is correct.
        Arguments:
          url (str): url to verify.
        """
        self.browser.switch_to_window(self.browser.window_handles[-1])
        # Assert that url in the browser is the same.
        # Please note that .org domain in href attribute of help anchor DOM element
        # is changed into .io domain. This is because browser is redirected from .org
        # domain to .io domain.
        self.assertEqual(self.get_url_with_changed_domain(url), self.browser.current_url)
        self.assertNotIn('Maze Found', self.browser.title)

    def verify_help_link(self, href):
        """
        Verifies that help link is correct
        Arguments:
            href (str): Help url
        """
        expected_link = {
            'href': href,
            'text': 'What does this mean?'
        }
        actual_link = self.cohort_management.get_cohort_help_element_and_click_help()

        self.assert_link(expected_link, actual_link)
        self.assert_opened_help_link_is_correct(href)

    def test_manual_cohort_help(self):
        """
        Scenario: Help in 'What does it mean?' is correct when we create cohort manually.
        Given that I am at 'Cohort' tab of LMS instructor dashboard
        And I check 'Enable Cohorts'
        And I add cohort name it, choose Manual for Cohort Assignment Method and
        No content group for Associated Content Group and save the cohort
        Then you see the UI text "Learners are added to this cohort only when..."
        followed by "What does this mean" link.
        And I click "What does this mean" link then help link should end with
        course_features/cohorts/cohort_config.html#assign-learners-to-cohorts-manually
        """
        self.cohort_management.add_cohort('cohort_name')

        href = 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/latest/' \
               'course_features/cohorts/cohort_config.html#assign-learners-to-cohorts-manually'

        self.verify_help_link(href)

    def test_automatic_cohort_help(self):
        """
        Scenario: Help in 'What does it mean?' is correct when we create cohort automatically.
        Given that I am at 'Cohort' tab of LMS instructor dashboard
        And I check 'Enable Cohorts'
        And I add cohort name it, choose Automatic for Cohort Assignment Method and
        No content group for Associated Content Group and save the cohort
        Then you see the UI text "Learners are added to this cohort automatically"
        followed by "What does this mean" link.
        And I click "What does this mean" link then help link should end with
        course_features/cohorts/cohorts_overview.html#all-automated-assignment
        """

        self.cohort_management.add_cohort('cohort_name', assignment_type='random')

        href = 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/latest/' \
               'course_features/cohorts/cohorts_overview.html#all-automated-assignment'

        self.verify_help_link(href)

    def enable_cohorting(self, course_fixture):
        """
        Enables cohorting for the current course.
        """
        url = LMS_BASE_URL + "/courses/" + course_fixture._course_key + '/cohorts/settings'  # pylint: disable=protected-access
        data = json.dumps({'is_cohorted': True})
        response = course_fixture.session.patch(url, data=data, headers=course_fixture.headers)
        self.assertTrue(response.ok, "Failed to enable cohorts")
