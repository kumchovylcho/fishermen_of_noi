from django.contrib.auth.models import User
from django.test import (TestCase,
                         Client,
                         )
from django.urls import reverse

from ribarite_na_noi.Braids.models import Braid


class TestDisplayBraids(TestCase):

    def create_two_braids(self):
        braid_1 = Braid.objects.create(name="gosen",
                                       thickness="#0.4",
                                       strength="4.2кг",
                                       length="150",
                                       is_colored=False,
                                       price=47,
                                       created_by=self.user
                                       )
        braid_2 = Braid.objects.create(name="gosen",
                                       thickness="#0.6",
                                       strength="6кг",
                                       length="150",
                                       is_colored=False,
                                       price=40,
                                       created_by=self.user
                                       )

        return braid_1, braid_2

    def setUp(self):
        self.client = Client()
        self.display_braids_url = reverse('display_braids')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )

    def test_display_braids_page_with_no_braids(self):
        response = self.client.get(self.display_braids_url)

        self.assertTemplateUsed(response,
                                "display-braids.html"
                                )

        self.assertEqual(len(response.context.get("all_braids")),
                         0
                         )

    def test_display_braids_order_by_price_ascending(self):
        braid_1, braid_2 = self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         braid_2.price
                         )

        self.assertEqual(queryset[1].price,
                         braid_1.price
                         )

    def test_display_braids_order_by_price_descending(self):
        braid_1, braid_2 = self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "-price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         braid_1.price
                         )

        self.assertEqual(queryset[1].price,
                         braid_2.price
                         )

    def test_display_braids_order_by_thickness_ascending(self):
        braid_1, braid_2 = self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "thickness"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].thickness,
                         braid_1.thickness
                         )

        self.assertEqual(queryset[1].thickness,
                         braid_2.thickness
                         )

    def test_display_braids_order_by_thickness_descending(self):
        braid_1, braid_2 = self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "-thickness"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].thickness,
                         braid_2.thickness
                         )

        self.assertEqual(queryset[1].thickness,
                         braid_1.thickness
                         )

    def test_display_braids_order_by_strength_ascending(self):
        braid_1, braid_2 = self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "strength"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].strength,
                         braid_1.strength
                         )

        self.assertEqual(queryset[1].strength,
                         braid_2.strength
                         )

    def test_display_braids_order_by_strength_descending(self):
        braid_1, braid_2 = self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "-strength"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].strength,
                         braid_2.strength
                         )

        self.assertEqual(queryset[1].strength,
                         braid_1.strength
                         )

    def test_display_braids_order_by_length_ascending(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.length = "200"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "length"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].length,
                         braid_2.length
                         )

        self.assertEqual(queryset[1].length,
                         braid_1.length
                         )

    def test_display_braids_order_by_length_descending(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.length = "200"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"sort_by": "-length"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].length,
                         braid_1.length
                         )

        self.assertEqual(queryset[1].length,
                         braid_2.length
                         )

    def test_display_braids_filter_by_thickness_0_2(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#0.2"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#0.2"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_0_3(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#0.3"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#0.3"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_0_4(self):
        self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#0.4"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_0_5(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#0.5"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#0.5"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_0_6(self):
        self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#0.6"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_0_8(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#0.8"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#0.8"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_1(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#1"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_1_2(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#1.2"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#1.2"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_1_5(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#1.5"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#1.5"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_thickness_2(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.thickness = "#2"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "#2"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_2_5_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "2.5кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "2.5кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_3_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "3кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "3кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_3_3_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "3.3кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "3.3кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_3_8_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "3.8кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "3.8кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_4_2_kg(self):
        self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "4.2кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_5_4_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "5.4кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "5.4кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_6_kg(self):
        self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "6кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_6_8_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "6.8кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "6.8кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_8_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "8кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "8кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_strength_10_kg(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.strength = "10кг"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "10кг"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_length_150_meters(self):
        self.create_two_braids()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "150"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         2
                         )

    def test_display_braids_filter_by_length_200_meters(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.length = "200"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "200"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_length_250_meters(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.length = "250"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "250"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_length_300_meters(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.length = "300"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "300"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_braids_filter_by_length_500_meters(self):
        braid_1, braid_2 = self.create_two_braids()
        braid_1.length = "500"
        braid_1.save()

        response = self.client.get(self.display_braids_url,
                                   {"filter_by": "500"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )


class TestCreateBraid(TestCase):

    def create_braid_obj(self):
        braid_info = dict(name="gosen",
                          thickness="#0.4",
                          strength="4.2кг",
                          length="150",
                          is_colored=False,
                          price=47,
                          created_by=self.user
                          )

        return braid_info

    def setUp(self):
        self.client = Client()
        self.create_braid_url = reverse('create_braid')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

    def test_successfully_create_braid(self):
        braid_data = self.create_braid_obj()

        response = self.client.post(self.create_braid_url,
                                    data=braid_data
                                    )

        braid = Braid.objects.get(price=47)

        self.assertRedirects(response,
                             reverse('display_braids')
                             )

        self.assertEqual(47,
                         braid.price
                         )

    def test_user_tries_to_reach_create_braid_page_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_braid_url)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response,
                             reverse('display_braids')
                             )

        self.assertTemplateNotUsed(response,
                                   "create-braid.html"
                                   )


class TestEditBraid(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.braid = Braid.objects.create(name="gosen",
                                          thickness="#0.4",
                                          strength="4.2кг",
                                          length="150",
                                          is_colored=False,
                                          price=47,
                                          created_by=self.user
                                          )

        self.edit_braid_url = reverse('edit_braid',
                                      kwargs={'pk': self.braid.pk}
                                      )

    def test_successfully_edit_braid_which_is_created_by_the_user(self):
        data_entered = dict(name="gosen",
                            thickness="#0.4",
                            strength="4.2кг",
                            length="150",
                            is_colored=False,
                            price=60,   # new price
                            created_by=self.user
                            )

        response = self.client.post(self.edit_braid_url,
                                    data=data_entered
                                    )

        self.braid.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_braids')
                             )

        self.assertEqual(self.braid.price,
                         60
                         )

        self.assertFalse(self.braid.price == 47)

    def test_user_tries_to_land_on_edit_braid_item_page_which_is_not_created_by_him(self):
        user_2 = User.objects.create_user(username="TamerTEST",
                                          password="pirata123"
                                          )

        self.client.logout()

        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_braid_url)

        self.assertRedirects(response,
                             reverse('display_braids')
                             )

        self.assertNotEqual(self.braid.created_by.pk,
                            user_2.pk
                            )

        self.assertTemplateNotUsed(response,
                                   "edit-braid.html"
                                   )

    def test_superuser_tries_to_land_on_edit_braid_item_page_which_is_not_created_by_him(self):
        superuser = User.objects.create_superuser(username="TamerSUPER",
                                                  password="pirata123"
                                                  )
        self.client.logout()

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_braid_url)

        self.assertNotEqual(self.braid.created_by.pk,
                            superuser.pk
                            )

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTemplateUsed(response,
                                "edit-braid.html"
                                )

    def test_not_logged_in_user_tries_to_land_on_edit_braid_page(self):
        self.client.logout()

        response = self.client.get(self.edit_braid_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse('display_braids')
                             )

        self.assertTemplateNotUsed(response,
                                   "edit-braid.html"
                                   )


class TestDeleteBraid(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.braid = Braid.objects.create(name="gosen",
                                          thickness="#0.4",
                                          strength="4.2кг",
                                          length="150",
                                          is_colored=False,
                                          price=47,
                                          created_by=self.user
                                          )

        self.delete_braid_url = reverse('delete_braid',
                                        kwargs={'pk': self.braid.pk}
                                        )

    def test_successfully_delete_braid_which_is_created_by_the_user(self):
        response = self.client.post(self.delete_braid_url)

        self.assertEqual(Braid.objects.filter(name="gosen").count(),
                         0
                         )

        self.assertRedirects(response,
                             reverse("display_braids")
                             )

    def test_not_logged_in_user_tries_to_reach_delete_braid_url(self):
        self.client.logout()

        response = self.client.get(self.delete_braid_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse("display_braids")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-braid.html"
                                   )

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_superuser_tries_to_reach_delete_braid_url_which_is_not_created_by_the_superuser(self):
        self.client.logout()

        User.objects.create_superuser(username="TamerSUPER",
                                      password="pirata123"
                                      )

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_braid_url)

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTrue(response.wsgi_request.user.is_superuser)

        self.assertTemplateUsed(response,
                                "delete-braid.html"
                                )

        self.assertNotEqual(response.wsgi_request.user.username,
                            self.braid.created_by.username
                            )

    def test_normal_logged_in_user_tries_to_reach_delete_braid_item_which_is_created_by_another_user(self):
        User.objects.create_user(username="TamerTEST",
                                 password="pirata123"
                                 )
        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_braid_url)

        self.assertTrue(response.status_code == 302)

        self.assertRedirects(response,
                             reverse("display_braids")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-braid.html"
                                   )
