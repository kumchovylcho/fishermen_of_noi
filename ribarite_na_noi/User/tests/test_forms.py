from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from ribarite_na_noi.User.forms import ChangeUsernameForm


class TestChangeUsernameForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )

    def test_successful_change_username(self):
        data = {
            "old_username": "Tamer",
            "new_username": "Pesho"
        }

        form = ChangeUsernameForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertIsNone(form.clean())

        form.save()

        self.user.refresh_from_db()

        self.assertEqual("Pesho", self.user.username)

    def test_user_enters_wrong_old_username(self):
        data = {
            "old_username": "Pesho",
            "new_username": "Tamer"
        }

        form = ChangeUsernameForm(data=data)

        self.assertFalse(form.is_valid())

        with self.assertRaises(ValidationError) as error:
            form.clean()

        self.assertEqual(*error.exception,
                         "Invalid old username"
                         )

    def test_user_tries_to_set_their_new_username_to_be_same_as_their_old_username(self):
        data = {
            "old_username": "Tamer",
            "new_username": "Tamer"
        }

        form = ChangeUsernameForm(data=data)

        self.assertFalse(form.is_valid())

        with self.assertRaises(ValidationError) as error:
            form.clean()

        self.assertEqual(*error.exception,
                         "New username cannot be same as old username"
                         )

    def test_user_tries_to_set_their_new_username_to_an_already_existing_username(self):
        User.objects.create_user(username="Pesho",
                                 password="pirata123"
                                 )

        data = {
            "old_username": "Tamer",
            "new_username": "Pesho"
        }

        form = ChangeUsernameForm(data=data)

        self.assertFalse(form.is_valid())

        with self.assertRaises(ValidationError) as error:
            form.clean()

        self.assertEqual(*error.exception,
                         "Username already exists"
                         )
