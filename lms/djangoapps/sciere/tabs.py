from courseware.tabs import CourseTab

class EnrolledTab(CourseTab):
    """
    A base class for any view types that require a user to be enrolled.
    """
    @classmethod
    def is_enabled(cls, course, user=None):
        """Returns true if this tab is enabled."""
        # return settings.FEATURES.get('NEW_TAB_ENABLED', False)
        return True

class ProfilesTab(CourseTab):
    """A new course tab."""

    name = "profiles_tab"
    title = ugettext_noop("Profiles")  # We don't have the user in this context, so we don't want to translate it at this level.
    view_name = "profiles_view"