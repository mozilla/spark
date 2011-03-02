from spark.tests import LocalizingClient, TestCase

from users.models import Profile
from users.tests import profile


class TestCaseBase(TestCase):
    """Base TestCase for the users app test cases."""

    def setUp(self):
        super(TestCaseBase, self).setUp()
        self.client = LocalizingClient()