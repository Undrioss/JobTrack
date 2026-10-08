
import unittest
import sqlite3
from unittest.mock import patch

from database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # Use a temporary in-memory database for each test.
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row

        # Redirect DatabaseManager to our test connection.
        self.patcher = patch(
            "database.sqlite3.connect",
            return_value=self.connection
        )
        self.patcher.start()

        self.db = DatabaseManager()

    def tearDown(self):
        self.db.close()
        self.patcher.stop()

    def add_sample_application(self):
        self.db.add_application(
            company="Test Company",
            position="Python Developer",
            location="Cape Town",
            salary="R25000",
            status="Applied",
            date_applied="2026-10-08",
            notes="Automated test"
        )

    def test_create_application(self):
        self.add_sample_application()

        applications = self.db.get_applications()

        self.assertEqual(len(applications), 1)
        self.assertEqual(
            applications[0]["company"],
            "Test Company"
        )

    def test_read_applications(self):
        self.add_sample_application()

        applications = self.db.get_applications()

        self.assertEqual(
            applications[0]["position"],
            "Python Developer"
        )

    def test_update_application(self):
        self.add_sample_application()

        applications = self.db.get_applications()
        application_id = applications[0]["id"]

        self.db.update_application(
            application_id,
            "Interview"
        )

        updated = self.db.get_applications()

        self.assertEqual(
            updated[0]["status"],
            "Interview"
        )

    def test_delete_application(self):
        self.add_sample_application()

        applications = self.db.get_applications()
        application_id = applications[0]["id"]

        self.db.delete_application(application_id)

        remaining = self.db.get_applications()

        self.assertEqual(len(remaining), 0)

    def test_empty_database(self):
        applications = self.db.get_applications()

        self.assertEqual(len(applications), 0)


if __name__ == "__main__":
    unittest.main()
