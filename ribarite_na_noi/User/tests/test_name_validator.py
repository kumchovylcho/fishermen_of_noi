from django.core.exceptions import ValidationError
from django.test import TestCase

from ribarite_na_noi.common.validators import validate_name


class TestUsername(TestCase):

    def test_valid_username(self):
        usernames = ("Tamer", "Tamer_", "55Tamer", "Tamer_55")

        for username in usernames:
            response = validate_name(username)
            self.assertIsNone(response)

    def test_invalid_username_with_more_than_one_underscore(self):
        usernames = ("__Tamer", "Tamer__", "Ta__mer", "_____")

        for username in usernames:
            with self.assertRaises(ValidationError) as error:
                validate_name(username)

            self.assertEqual(*error.exception,
                             "You can't use only underscores or have more than one underscore"
                             )

    def test_invalid_username_with_forbidden_symbols(self):
        from string import punctuation

        usernames = [f"Tamer{symbol}" for symbol in punctuation if symbol != "_"]

        for username in usernames:
            with self.assertRaises(ValidationError) as error:
                validate_name(username)

            self.assertEqual(*error.exception,
                             "You can only use letters, numbers and underscores"
                             )
