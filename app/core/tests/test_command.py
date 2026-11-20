

from psycopg2 import OperationalError as psycopg2OpError
from django.db.utils import OperationalError
from django.core.management import call_command
from django.test import SimpleTestCase
from unittest.mock import patch


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):

    def test_wait_for_command(self, pathed_check):
        pathed_check.return_value = True

        call_command("wait_for_db")

        pathed_check.assert_called_once_with(databases=['default'])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, pathed_check):
        pathed_check.side_effect = [psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(pathed_check.call_count, 6)
        pathed_check.assert_called_with(databases=['default'])
