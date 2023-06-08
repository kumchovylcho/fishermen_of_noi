from django.contrib.auth.models import User
from django.test import (TestCase,
                         Client,
                         )
from django.urls import reverse

from ribarite_na_noi.Reels.models import Reel


class TestDisplayReels(TestCase):

    def create_two_reels(self):
        reel_1 = Reel.objects.create(size="3000",
                                     gear_ratio="5:1",
                                     model="shimano",
                                     weight=205,
                                     bearings=12,
                                     price=1000,
                                     created_by=self.user
                                     )
        reel_2 = Reel.objects.create(size="3000",
                                     gear_ratio="5:1",
                                     model="shimano",
                                     weight=205,
                                     bearings=12,
                                     price=950,
                                     created_by=self.user
                                     )

        return reel_1, reel_2

    def setUp(self):
        self.client = Client()
        self.display_reels_url = reverse('display_reels')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )

    def test_display_reels_page_with_no_reels(self):
        response = self.client.get(self.display_reels_url)

        self.assertTemplateUsed(response,
                                "display-reels.html"
                                )

        self.assertEqual(len(response.context.get("all_reels")),
                         0
                         )

    def test_display_reels_order_by_price_ascending(self):
        reel_1, reel_2 = self.create_two_reels()

        response = self.client.get(self.display_reels_url,
                                   {"sort_by": "price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         reel_2.price
                         )

        self.assertEqual(queryset[1].price,
                         reel_1.price
                         )

    def test_display_reels_order_by_price_descending(self):
        reel_1, reel_2 = self.create_two_reels()

        response = self.client.get(self.display_reels_url,
                                   {"sort_by": "-price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         reel_1.price
                         )

        self.assertEqual(queryset[1].price,
                         reel_2.price
                         )

    def test_display_reels_order_by_size_ascending(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size, reel_2.size = "3000", "4000"

        reel_1.save()
        reel_2.save()

        reel_1.refresh_from_db()
        reel_2.refresh_from_db()

        response = self.client.get(self.display_reels_url,
                                   {"sort_by": "size"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].size,
                         reel_1.size
                         )

        self.assertEqual(queryset[1].size,
                         reel_2.size
                         )

    def test_display_reels_order_by_size_descending(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size, reel_2.size = "3000", "4000"

        reel_1.save()
        reel_2.save()

        reel_1.refresh_from_db()
        reel_2.refresh_from_db()

        response = self.client.get(self.display_reels_url,
                                   {"sort_by": "-size"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].size,
                         reel_2.size
                         )

        self.assertEqual(queryset[1].size,
                         reel_1.size
                         )

    def test_display_reels_order_by_gear_ratio_ascending(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio, reel_2.gear_ratio = "5:1", "6.2:1"

        reel_1.save()
        reel_2.save()

        reel_1.refresh_from_db()
        reel_2.refresh_from_db()

        response = self.client.get(self.display_reels_url,
                                   {"sort_by": "gear_ratio"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].gear_ratio,
                         reel_1.gear_ratio
                         )

        self.assertEqual(queryset[1].gear_ratio,
                         reel_2.gear_ratio
                         )

    def test_display_reels_order_by_gear_ratio_descending(self):
        rod_1, rod_2 = self.create_two_reels()
        rod_1.action, rod_2.action = "5:1", "6.2:1"

        rod_1.save()
        rod_2.save()

        rod_1.refresh_from_db()
        rod_2.refresh_from_db()

        response = self.client.get(self.display_reels_url,
                                   {"sort_by": "-gear_ratio"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].gear_ratio,
                         rod_2.gear_ratio
                         )

        self.assertEqual(queryset[1].gear_ratio,
                         rod_1.gear_ratio
                         )

    def test_display_reels_filter_by_size_1000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "1000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "1000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_size_2000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "2000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "2000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_size_3000(self):
        self.create_two_reels()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "3000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         2
                         )

    def test_display_reels_filter_by_size_4000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "4000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "4000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_size_5000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "5000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "5000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_size_6000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "6000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "6000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_size_7000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "7000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "7000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_size_8000(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.size = "8000"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "8000"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_4_2_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "4.2:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "4.2:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_4_9_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "4.9:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "4.9:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_5_1(self):
        self.create_two_reels()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "5:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         2
                         )

    def test_display_reels_filter_by_gear_ratio_5_2_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "5.2:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "5.2:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_5_3_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "5.3:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "5.3:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_5_4_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "5.4:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "5.4:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_5_7_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "5.7:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "5.7:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_6_1_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "6.1:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "6.1:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_6_2_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "6.2:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "6.2:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_reels_filter_by_gear_ratio_6_5_1(self):
        reel_1, reel_2 = self.create_two_reels()
        reel_1.gear_ratio = "6.5:1"

        reel_1.save()

        response = self.client.get(self.display_reels_url,
                                   {"filter_by": "6.5:1"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )


class TestCreateReel(TestCase):

    def create_reel_obj(self):
        reel_info = {"size": "3000",
                     "gear_ratio": "5:1",
                     "model": "shimano",
                     "weight": 205,
                     "bearings": 12,
                     "price": 1000,
                     "created_by": self.user
                     }

        return reel_info

    def setUp(self):
        self.client = Client()
        self.create_reel_url = reverse('create_reel')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

    def test_successfully_create_reel(self):
        reel_data = self.create_reel_obj()

        response = self.client.post(self.create_reel_url,
                                    data=reel_data
                                    )

        reel = Reel.objects.get(model="shimano")
        reel.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_reels')
                             )

        self.assertEqual("shimano",
                         reel.model
                         )

    def test_user_tries_to_reach_create_rod_page_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_reel_url)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response,
                             reverse('display_reels')
                             )

        self.assertTemplateNotUsed(response,
                                   "create-reel"
                                   )


class TestEditReel(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.reel = Reel.objects.create(size="3000",
                                        gear_ratio="5:1",
                                        model="shimano",
                                        weight=205,
                                        bearings=12,
                                        price=1000,
                                        created_by=self.user
                                        )

        self.edit_reel_url = reverse('edit_reel',
                                     kwargs={'pk': self.reel.pk}
                                     )

    def test_successfully_edit_reel_which_is_created_by_the_user(self):
        data_entered = dict(size="3000",
                            gear_ratio="5:1",
                            model="shimano",
                            weight=205,
                            bearings=12,
                            price=850,
                            created_by=self.user
                            )

        response = self.client.post(self.edit_reel_url,
                                    data=data_entered
                                    )

        self.reel.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_reels')
                             )

        self.assertEqual(self.reel.price,
                         850
                         )

        self.assertFalse(self.reel.price == 1000)

    def test_user_tries_to_land_on_edit_reel_item_page_which_is_not_created_by_him(self):
        user_2 = User.objects.create_user(username="TamerTEST",
                                          password="pirata123"
                                          )

        self.client.logout()

        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_reel_url)

        self.assertRedirects(response,
                             reverse('display_reels')
                             )

        self.assertNotEqual(self.reel.created_by.pk,
                            user_2.pk
                            )

        self.assertTemplateNotUsed(response,
                                   "edit-reel.html"
                                   )

    def test_superuser_tries_to_land_on_edit_reel_item_page_which_is_not_created_by_him(self):
        superuser = User.objects.create_superuser(username="TamerSUPER",
                                                  password="pirata123"
                                                  )
        self.client.logout()

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_reel_url)

        self.assertNotEqual(self.reel.created_by.pk,
                            superuser.pk
                            )

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTemplateUsed(response,
                                "edit-reel.html"
                                )

    def test_not_logged_in_user_tries_to_land_on_edit_item_page(self):
        self.client.logout()

        response = self.client.get(self.edit_reel_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse('display_reels')
                             )

        self.assertTemplateNotUsed(response,
                                   "edit-reel.html"
                                   )


class TestDeleteReel(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.reel = Reel.objects.create(size="3000",
                                        gear_ratio="5:1",
                                        model="shimano",
                                        weight=205,
                                        bearings=12,
                                        price=850,
                                        created_by=self.user
                                        )

        self.delete_reel_url = reverse('delete_reel',
                                       kwargs={'pk': self.reel.pk}
                                       )

    def test_successfully_delete_reel_which_is_created_by_the_user(self):
        response = self.client.post(self.delete_reel_url)

        self.assertEqual(Reel.objects.filter(model="shimano").count(),
                         0
                         )

        self.assertRedirects(response,
                             reverse("display_reels")
                             )

    def test_not_logged_in_user_tries_to_reach_delete_reel_url(self):
        self.client.logout()

        response = self.client.get(self.delete_reel_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse("display_reels")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-reel.html"
                                   )

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_superuser_tries_to_reach_delete_reel_url_which_is_not_created_by_the_superuser(self):
        self.client.logout()

        User.objects.create_superuser(username="TamerSUPER",
                                      password="pirata123"
                                      )

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_reel_url)

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTrue(response.wsgi_request.user.is_superuser)

        self.assertTemplateUsed(response,
                                "delete-reel.html"
                                )

        self.assertNotEqual(response.wsgi_request.user.username,
                            self.reel.created_by.username
                            )

    def test_normal_logged_in_user_tries_to_reach_reel_which_is_created_by_another_user(self):
        User.objects.create_user(username="TamerTEST",
                                 password="pirata123"
                                 )
        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_reel_url)

        self.assertTrue(response.status_code == 302)

        self.assertRedirects(response,
                             reverse("display_reels")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-reel.html"
                                   )
