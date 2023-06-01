from django.contrib.auth.models import User
from django.test import (TestCase,
                         Client,
                         )
from django.urls import reverse

from ribarite_na_noi.Rods.models import Rod


class TestDisplayRods(TestCase):

    def create_two_rods(self):
        rod_1 = Rod.objects.create(rod_type="Мач",
                                   length=4,
                                   guides=10,
                                   rod_name="viper",
                                   action="20-40",
                                   color="black",
                                   price=200,
                                   created_by=self.user
                                   )
        rod_2 = Rod.objects.create(rod_type="Мач",
                                   length=4,
                                   guides=10,
                                   rod_name="viper",
                                   action="20-40",
                                   color="black",
                                   price=150,
                                   created_by=self.user
                                   )

        return rod_1, rod_2

    def setUp(self):
        self.client = Client()
        self.display_rods_url = reverse('display_rods')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )

    def test_display_rod_page_with_no_rods(self):
        response = self.client.get(self.display_rods_url)

        self.assertTemplateUsed(response,
                                "display-rods.html"
                                )

        self.assertEqual(len(response.context.get("all_rods")),
                         0
                         )

    def test_display_rods_order_by_price_ascending(self):
        rod_1, rod_2 = self.create_two_rods()

        response = self.client.get(self.display_rods_url,
                                   {"sort_by": "price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         rod_2.price
                         )

        self.assertEqual(queryset[1].price,
                         rod_1.price
                         )

    def test_display_rods_order_by_price_descending(self):
        rod_1, rod_2 = self.create_two_rods()

        response = self.client.get(self.display_rods_url,
                                   {"sort_by": "-price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         rod_1.price
                         )

        self.assertEqual(queryset[1].price,
                         rod_2.price
                         )

    def test_display_rods_order_by_length_ascending(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.length, rod_2.length = 3, 5

        rod_1.save()
        rod_2.save()

        rod_1.refresh_from_db()
        rod_2.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"sort_by": "length"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].length,
                         rod_1.length
                         )

        self.assertEqual(queryset[1].length,
                         rod_2.length
                         )

    def test_display_rods_order_by_length_descending(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.length, rod_2.length = 3, 5

        rod_1.save()
        rod_2.save()

        rod_1.refresh_from_db()
        rod_2.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"sort_by": "-length"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].length,
                         rod_2.length
                         )

        self.assertEqual(queryset[1].length,
                         rod_1.length
                         )

    def test_display_rods_order_by_action_ascending(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action, rod_2.action = "1-5", "1-8"

        rod_1.save()
        rod_2.save()

        rod_1.refresh_from_db()
        rod_2.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"sort_by": "action"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].length,
                         rod_1.length
                         )

        self.assertEqual(queryset[1].length,
                         rod_2.length
                         )

    def test_display_rods_order_by_action_descending(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action, rod_2.action = "1-8", "1-5"

        rod_1.save()
        rod_2.save()

        rod_1.refresh_from_db()
        rod_2.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"sort_by": "-action"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].length,
                         rod_2.length
                         )

        self.assertEqual(queryset[1].length,
                         rod_1.length
                         )

    def test_display_rods_filter_by_match(self):
        self.create_two_rods()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "Мач"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         2
                         )

    def test_display_rods_filter_by_telematch(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.rod_type = "Телемач"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "Телемач"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_telescope(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.rod_type = "Телескоп"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "Телескоп"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_spinning(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.rod_type = "Спининг"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "Спининг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_action_1_5(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action = "1-5"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "1-5"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_action_1_8(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action = "1-8"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "1-8"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_action_5_12(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action = "5-12"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "5-12"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_action_10_27(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action = "10-27"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "10-27"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_action_20_40(self):
        self.create_two_rods()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "20-40"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         2
                         )

    def test_display_rods_filter_by_action_10_50(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action = "10-50"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "10-50"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_rods_filter_by_action_40_80(self):
        rod_1, rod_2 = self.create_two_rods()
        rod_1.action = "40-80"

        rod_1.save()
        rod_1.refresh_from_db()

        response = self.client.get(self.display_rods_url,
                                   {"filter_by": "40-80"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )


class TestCreateRod(TestCase):

    def create_rod_obj(self):
        rod_info = {"rod_type": "Мач",
                    "length": 4,
                    "guides": 10,
                    "rod_name": "viper",
                    "action": "20-40",
                    "color": "black",
                    "price": 200,
                    "created_by": self.user
                    }

        return rod_info

    def setUp(self):
        self.client = Client()
        self.create_rod_url = reverse('create_rod')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

    def test_successfully_create_rod(self):
        rod_data = self.create_rod_obj()

        response = self.client.post(self.create_rod_url,
                                    data=rod_data
                                    )

        rod = Rod.objects.get(rod_name="viper")
        rod.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_rods')
                             )

        self.assertEqual("viper",
                         rod.rod_name
                         )

    def test_user_tries_to_reach_create_rod_page_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_rod_url)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response,
                             reverse('display_rods')
                             )


class TestEditRod(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.rod = Rod.objects.create(rod_type="Мач",
                                      length=4,
                                      guides=10,
                                      rod_name="viper",
                                      action="20-40",
                                      color="black",
                                      price=200,
                                      created_by=self.user
                                      )

        self.edit_rod_url = reverse('edit_rod',
                                    kwargs={'pk': self.rod.pk}
                                    )

    def test_successfully_edit_rod_which_is_created_by_the_user(self):
        data_entered = {"rod_type": "Мач",
                        "length": 4,
                        "guides": 10,
                        "rod_name": "viper",
                        "action": "20-40",
                        "color": "black",
                        "price": 150,  # new price
                        "created_by": self.user
                        }

        response = self.client.post(self.edit_rod_url,
                                    data=data_entered
                                    )

        self.rod.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_rods')
                             )

        self.assertEqual(self.rod.price,
                         150
                         )

    def test_user_tries_to_land_on_edit_item_page_which_is_not_created_by_him(self):
        user_2 = User.objects.create_user(username="TamerTEST",
                                          password="pirata123"
                                          )

        self.client.logout()

        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_rod_url)

        self.assertRedirects(response,
                             reverse('display_rods')
                             )

        self.assertNotEqual(self.rod.created_by.pk,
                            user_2.pk
                            )

        self.assertTemplateNotUsed(response,
                                   "edit-rod.html"
                                   )

    def test_superuser_tries_to_land_on_edit_item_page_which_is_not_created_by_him(self):
        superuser = User.objects.create_superuser(username="TamerSUPER",
                                                  password="pirata123"
                                                  )
        self.client.logout()

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_rod_url)

        self.assertNotEqual(self.rod.created_by.pk,
                            superuser.pk
                            )

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTemplateUsed(response,
                                "edit-rod.html"
                                )

    def test_not_logged_in_user_tries_to_land_on_edit_item_page(self):
        self.client.logout()

        response = self.client.get(self.edit_rod_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse('display_rods')
                             )


class TestDeleteRod(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.rod = Rod.objects.create(rod_type="Мач",
                                      length=4,
                                      guides=10,
                                      rod_name="viper",
                                      action="20-40",
                                      color="black",
                                      price=200,
                                      created_by=self.user
                                      )

        self.delete_rod_url = reverse('delete_rod',
                                      kwargs={'pk': self.rod.pk}
                                      )

    def test_successfully_delete_rod_which_is_created_by_the_user(self):
        response = self.client.post(self.delete_rod_url)

        self.assertEqual(Rod.objects.filter(rod_name="viper").count(),
                         0
                         )

        self.assertRedirects(response,
                             reverse("display_rods")
                             )

    def test_not_logged_in_user_tries_to_reach_delete_rod_url(self):
        self.client.logout()

        response = self.client.get(self.delete_rod_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse("display_rods")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-rod.html"
                                   )

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_superuser_tries_to_reach_delete_rod_url_which_is_not_created_by_the_superuser(self):
        self.client.logout()

        User.objects.create_superuser(username="TamerSUPER",
                                      password="pirata123"
                                      )

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_rod_url)

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTrue(response.wsgi_request.user.is_superuser)

        self.assertTemplateUsed(response,
                                "delete-rod.html"
                                )

        self.assertNotEqual(response.wsgi_request.user.username,
                            self.rod.created_by.username)

    def test_normal_logged_in_user_tries_to_reach_rod_which_is_created_by_another_user(self):
        User.objects.create_user(username="TamerTEST",
                                 password="pirata123"
                                 )
        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_rod_url)

        self.assertTrue(response.status_code == 302)

        self.assertRedirects(response,
                             reverse("display_rods")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-rod.html"
                                   )