from django.contrib.auth.models import User
from django.test import (TestCase,
                         Client,
                         )
from django.urls import reverse


class TestUserLogInView(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

        self.username = "Tamer"
        self.password = "pirata123"

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_successful_user_login(self):
        response = self.client.post(
            self.login_url,
            {"username": self.username,
             "password": self.password,
             },
        )

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_user_login_with_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {"username": "invalid",
             "password": "pirata123",
             },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, 'login.html')

    def user_tries_to_reach_login_page_when_he_is_already_logged_in(self):
        self.client.post(
            self.login_url,
            {"username": "Tamer",
             "password": "pirata123",
             },
        )

        response = self.client.get(
            self.login_url,
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)


class TestLogoutView(TestCase):

    def test_successful_logout(self):
        self.client = Client()
        self.logout_url = reverse('logout')

        self.username = "Tamer"
        self.password = "pirata123"

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(
            self.logout_url,
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_when_user_is_not_logged_in(self):
        self.client = Client()
        self.logout_url = reverse('logout')

        response = self.client.post(
            self.logout_url
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('home')
                             )


class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_successful_user_registration(self):
        response = self.client.post(self.register_url,
                                    {
                                        'username': "Tamer",
                                        'password1': "pirata123",
                                        'password2': "pirata123"
                                    }
                                    )

        self.assertRedirects(response, reverse('welcome-page'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(User.objects.filter(username="Tamer").count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_unsuccessful_user_registration_with_different_passwords(self):
        response = self.client.post(self.register_url,
                                    {
                                        'username': "Tamer",
                                        'password1': "pirata123",
                                        'password2': "pirata132"  # password is different from `password1`
                                    }
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_tries_to_register_with_already_existing_username(self):
        User.objects.create_user(username="Tamer", password="pirata123")

        response = self.client.post(self.register_url,
                                    {
                                        'username': "Tamer",
                                        'password1': "pirata123",
                                        'password2': "pirata123"
                                    }
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="Tamer").count(), 1)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_tries_to_reach_registration_form_when_logged_in(self):
        User.objects.create_user(username="Tamer", password="pirata123")

        login_url = reverse('login')
        self.client.post(
            login_url,
            {"username": "Tamer",
             "password": "pirata123",
             },
        )

        response = self.client.get(
            self.register_url,
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)


class TestProfileView(TestCase):

    def setUp(self):
        self.client = Client()

        self.username = "Tamer"
        self.password = "pirata123"

        self.user = User.objects.create_user(username=self.username,
                                             password=self.password
                                             )

        self.client.login(username=self.username,
                          password=self.password
                          )

        self.profile_view_url = reverse('profile',
                                        kwargs={'pk': self.user.pk}
                                        )

    def test_successful_land_on_profile_view_page(self):
        response = self.client.get(
            self.profile_view_url,
        )

        self.assertEqual(sum(response.context['all_posts'].values()),
                         0
                         )

        self.assertEqual(response.context['created_items'],
                         0
                         )

        self.assertTemplateUsed(response,
                                "profile.html"
                                )

    def test_logged_in_user_tries_to_land_on_another_user_profile(self):
        User.objects.create_user(username="Tamer2",
                                 password="pirata123"
                                 )
        self.client.login(username="Tamer2",
                          password="pirata123"
                          )

        self.profile_view_url = reverse('profile',
                                        kwargs={'pk': self.user.pk}
                                        )

        response = self.client.get(self.profile_view_url)

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertNotEqual(response.wsgi_request.user.pk,
                            self.user.pk
                            )

    def test_not_logged_in_user_tries_to_access_someones_user_profile(self):
        self.client.logout()

        response = self.client.get(self.profile_view_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse('login')
                             )


class TestUserChangeUsername(TestCase):

    def setUp(self):
        self.client = Client()

        self.username = "Tamer"
        self.password = "pirata123"

        self.user = User.objects.create_user(username=self.username,
                                             password=self.password
                                             )
        self.client.login(username=self.username,
                          password=self.password
                          )

        self.change_username_url = reverse('change_username',
                                           kwargs={'pk': self.user.pk}
                                           )

    def test_successfully_change_username(self):
        new_username = "TamerNEW"

        response = self.client.post(self.change_username_url,
                                    {'old_username': self.user.username,
                                     'new_username': new_username
                                     }
                                    )

        self.user.refresh_from_db()

        self.assertEqual(self.user.username,
                         new_username
                         )

        self.assertRedirects(response,
                             reverse('successful_username_change')
                             )

        self.assertEqual(response.status_code, 302)

    def test_other_user_tries_to_land_on_current_user_change_username_page(self):
        User.objects.create_user(username="Tamer2",
                                 password="pirata123"
                                 )
        self.client.login(username="Tamer2",
                          password="pirata123"
                          )

        self.profile_view_url = reverse('change_username',
                                        kwargs={'pk': self.user.pk}
                                        )

        response = self.client.get(self.profile_view_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertNotEqual(response.wsgi_request.user.pk,
                            self.user.pk
                            )

    def test_not_logged_in_user_tries_to_access_change_username_page(self):
        self.client.logout()

        response = self.client.get(self.change_username_url)

        self.assertRedirects(response,
                             reverse('login')
                             )

        self.assertEqual(response.status_code,
                         302
                         )

    def test_user_tries_to_enter_old_username_which_already_exists_on_other_user(self):
        second_user = User.objects.create_user(username="Pesho",
                                               password="pirata123"
                                               )
        data_entered = {"old_username": "Pesho",
                        "new_username": "TamerNEW"
                        }

        # Tamer tries to enter old username as `Pesho` and tries to set Pesho's username to `TamerNEW`
        response = self.client.post(self.change_username_url,
                                    data=data_entered
                                    )

        self.assertRedirects(response,
                             reverse('profile',
                                     kwargs={"pk": self.user.pk}
                                     )
                             )
        self.assertEqual(response.status_code,
                         302
                         )
        self.user.refresh_from_db()

        self.assertEqual(self.user.username,
                         "Tamer"
                         )
        self.assertEqual(second_user.username,
                         "Pesho"
                         )


class TestDeleteUser(TestCase):

    def setUp(self):
        self.client = Client()

        self.username = "Tamer"
        self.password = "pirata123"

        self.user = User.objects.create_user(username=self.username,
                                             password=self.password
                                             )
        self.client.login(username=self.username,
                          password=self.password
                          )

        self.delete_username_url = reverse('delete_user',
                                           kwargs={'pk': self.user.pk}
                                           )

    def test_successfully_delete_user(self):
        response = self.client.post(self.delete_username_url)

        self.assertTrue(User.objects.filter(username=self.username).count() == 0)
        self.assertRedirects(response,
                             reverse('home')
                             )

    def test_not_logged_in_user_tries_to_reach_delete_profile_page(self):
        self.client.logout()

        response = self.client.get(self.delete_username_url,
                                   kwargs={'pk': 1}  # first user is always with PK 1
                                   )

        self.assertRedirects(response,
                             reverse('login')
                             )

        self.assertEqual(response.status_code,
                         302
                         )

    def test_user_tries_to_land_on_another_user_deletion_page(self):
        User.objects.create_user(username="Tamer2",
                                 password="pirata123"
                                 )
        self.client.login(username="Tamer2",
                          password="pirata123"
                          )

        self.delete_user_view_url = reverse('delete_user',
                                            kwargs={'pk': self.user.pk}
                                            )

        response = self.client.get(self.delete_user_view_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertNotEqual(response.wsgi_request.user.pk,
                            self.user.pk
                            )

    def test_if_deletion_message_is_shown_on_screen_before_the_user_deletes_his_profile(self):
        response = self.client.get(self.delete_username_url,
                                   kwargs={'pk': self.user.pk}
                                   )

        self.assertEqual("Наистина ли искаш да си изтриеш профила ?",
                         response.context["delete_user_msg"]
                         )
