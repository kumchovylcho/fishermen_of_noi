from django.contrib.auth.models import User
from django.test import (TestCase,
                         Client,
                         )
from django.urls import reverse

from ribarite_na_noi.Chepareta.models import Chepare


class TestDisplayChepareta(TestCase):

    def create_two_chepare(self):
        chepare_1 = Chepare.objects.create(type="За сафрид",
                                           number_of_hooks="12",
                                           hook_number="10",
                                           main_line_thickness=0.23,
                                           semi_main_line_thickness=0.18,
                                           color="Черга",
                                           price=5,
                                           created_by=self.user
                                           )
        chepare_2 = Chepare.objects.create(type="За чернокоп",
                                           number_of_hooks="10",
                                           hook_number="05",
                                           main_line_thickness=0.27,
                                           semi_main_line_thickness=0.23,
                                           color="Черга",
                                           price=8,
                                           created_by=self.user
                                           )

        return chepare_1, chepare_2

    def setUp(self):
        self.client = Client()
        self.display_chepareta_url = reverse('display_chepareta')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )

    def test_display_chepareta_page_with_no_chepareta(self):
        response = self.client.get(self.display_chepareta_url)

        self.assertTemplateUsed(response,
                                "display-chepareta.html"
                                )

        self.assertEqual(len(response.context.get("all_chepareta")),
                         0
                         )

    def test_display_chepareta_order_by_price_ascending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         chepare_1.price
                         )

        self.assertEqual(queryset[1].price,
                         chepare_2.price
                         )

    def test_display_chepareta_order_by_price_descending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "-price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         chepare_2.price
                         )

        self.assertEqual(queryset[1].price,
                         chepare_1.price
                         )

    def test_display_chepareta_order_by_number_of_hooks_ascending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "number_of_hooks"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].number_of_hooks,
                         chepare_2.number_of_hooks
                         )

        self.assertEqual(queryset[1].number_of_hooks,
                         chepare_1.number_of_hooks
                         )

    def test_display_leads_order_by_lead_type_descending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "-number_of_hooks"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].number_of_hooks,
                         chepare_1.number_of_hooks
                         )

        self.assertEqual(queryset[1].number_of_hooks,
                         chepare_2.number_of_hooks
                         )

    def test_display_chepareta_order_by_hook_number_ascending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "hook_number"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].hook_number,
                         chepare_2.hook_number
                         )

        self.assertEqual(queryset[1].hook_number,
                         chepare_1.hook_number
                         )

    def test_display_chepareta_order_by_hook_number_descending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "-hook_number"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].hook_number,
                         chepare_1.hook_number
                         )

        self.assertEqual(queryset[1].hook_number,
                         chepare_2.hook_number
                         )

    def test_display_chepareta_order_by_main_line_thickness_ascending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "main_line_thickness"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].main_line_thickness,
                         chepare_1.main_line_thickness
                         )

        self.assertEqual(queryset[1].main_line_thickness,
                         chepare_2.main_line_thickness
                         )

    def test_display_chepareta_order_by_main_line_thickness_descending(self):
        chepare_1, chepare_2 = self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"sort_by": "-main_line_thickness"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].main_line_thickness,
                         chepare_2.main_line_thickness
                         )

        self.assertEqual(queryset[1].main_line_thickness,
                         chepare_1.main_line_thickness
                         )

    def test_display_chepareta_filter_by_type_safrid(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "За сафрид"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_type_chernokop(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "За чернокоп"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_type_karagyoz(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.type = "За карагьоз"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "За карагьоз"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_type_palamud(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.type = "За паламуд"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "За паламуд"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_number_of_hooks_10(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "10"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_number_of_hooks_12(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "12"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_number_of_hooks_14(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.number_of_hooks = "14"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "14"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_number_of_hooks_16(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.number_of_hooks = "16"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "16"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_number_of_hooks_18(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.number_of_hooks = "18"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "18"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_number_of_hooks_20(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.number_of_hooks = "20"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "20"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_12(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "12"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_11(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "11"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "11"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_10(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "10"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_09(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "09"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "09"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_08(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "08"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "08"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_07(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "07"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "07"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_06(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "06"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "06"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_05(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "05"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_04(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "04"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "04"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_03(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "03"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "03"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_02(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "02"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "02"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_hook_number_01(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.hook_number = "01"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "01"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_chepare_color_cherga(self):
        self.create_two_chepare()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "Черга"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         2
                         )

    def test_display_chepareta_filter_by_chepare_color_green(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.color = "Зелено"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "Зелено"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_chepare_color_yellow(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.color = "Жълто"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "Жълто"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_chepare_color_blue(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.color = "Синьо"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "Синьо"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_chepare_color_red(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.color = "Червено"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "Червено"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_chepareta_filter_by_chepare_color_pumpkin(self):
        chepare_1, chepare_2 = self.create_two_chepare()
        chepare_1.color = "Тиква"
        chepare_1.save()

        response = self.client.get(self.display_chepareta_url,
                                   {"filter_by": "Тиква"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )


class TestCreateChepare(TestCase):

    def create_lead_obj(self):
        chepare_info = dict(type="За сафрид",
                            number_of_hooks="12",
                            hook_number="10",
                            main_line_thickness=0.23,
                            semi_main_line_thickness=0.18,
                            color="Черга",
                            price=5,
                            created_by=self.user
                            )

        return chepare_info

    def setUp(self):
        self.client = Client()
        self.create_chepare_url = reverse('create_chepare')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

    def test_successfully_create_chepare(self):
        chepare_data = self.create_lead_obj()

        response = self.client.post(self.create_chepare_url,
                                    data=chepare_data
                                    )

        chepare = Chepare.objects.get(price=5)

        self.assertRedirects(response,
                             reverse('display_chepareta')
                             )

        self.assertEqual(5,
                         chepare.price
                         )

    def test_user_tries_to_reach_create_chepare_page_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_chepare_url)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response,
                             reverse('display_chepareta')
                             )

        self.assertTemplateNotUsed(response,
                                   "create-chepare.html"
                                   )


class TestEditChepare(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.chepare = Chepare.objects.create(type="За сафрид",
                                              number_of_hooks="12",
                                              hook_number="10",
                                              main_line_thickness=0.23,
                                              semi_main_line_thickness=0.18,
                                              color="Черга",
                                              price=5,
                                              created_by=self.user
                                              )

        self.edit_chepare_url = reverse('edit_chepare',
                                        kwargs={'pk': self.chepare.pk}
                                        )

    def test_successfully_edit_chepare_which_is_created_by_the_user(self):
        data_entered = dict(type="За сафрид",
                            number_of_hooks="12",
                            hook_number="08",  # new hook number
                            main_line_thickness=0.23,
                            semi_main_line_thickness=0.18,
                            color="Черга",
                            price=9,  # new price
                            created_by=self.user
                            )

        response = self.client.post(self.edit_chepare_url,
                                    data=data_entered
                                    )

        self.chepare.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_chepareta')
                             )

        self.assertEqual(self.chepare.hook_number,
                         "08"
                         )

        self.assertEqual(self.chepare.price,
                         9
                         )

        self.assertFalse(self.chepare.price == 5)
        self.assertFalse(self.chepare.hook_number == "10")

    def test_user_tries_to_land_on_edit_chepare_item_page_which_is_not_created_by_him(self):
        user_2 = User.objects.create_user(username="TamerTEST",
                                          password="pirata123"
                                          )

        self.client.logout()

        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_chepare_url)

        self.assertRedirects(response,
                             reverse('display_chepareta')
                             )

        self.assertNotEqual(self.chepare.created_by.pk,
                            user_2.pk
                            )

        self.assertTemplateNotUsed(response,
                                   "edit-chepare.html"
                                   )

    def test_superuser_tries_to_land_on_edit_chepare_item_page_which_is_not_created_by_him(self):
        superuser = User.objects.create_superuser(username="TamerSUPER",
                                                  password="pirata123"
                                                  )
        self.client.logout()

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_chepare_url)

        self.assertNotEqual(self.chepare.created_by.pk,
                            superuser.pk
                            )

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTemplateUsed(response,
                                "edit-chepare.html"
                                )

    def test_not_logged_in_user_tries_to_land_on_edit_chepare_page(self):
        self.client.logout()

        response = self.client.get(self.edit_chepare_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse('display_chepareta')
                             )

        self.assertTemplateNotUsed(response,
                                   "edit-chepare.html"
                                   )


class TestDeleteChepare(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.chepare = Chepare.objects.create(type="За сафрид",
                                              number_of_hooks="12",
                                              hook_number="10",
                                              main_line_thickness=0.23,
                                              semi_main_line_thickness=0.18,
                                              color="Черга",
                                              price=5,
                                              created_by=self.user
                                              )

        self.delete_chepare_url = reverse('delete_chepare',
                                          kwargs={'pk': self.chepare.pk}
                                          )

    def test_successfully_delete_chepare_which_is_created_by_the_user(self):
        response = self.client.post(self.delete_chepare_url)

        self.assertEqual(Chepare.objects.filter(type="За сафрид").count(),
                         0
                         )

        self.assertRedirects(response,
                             reverse("display_chepareta")
                             )

    def test_not_logged_in_user_tries_to_reach_delete_chepare_url(self):
        self.client.logout()

        response = self.client.get(self.delete_chepare_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse("display_chepareta")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-chepare.html"
                                   )

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_superuser_tries_to_reach_delete_chepare_url_which_is_not_created_by_the_superuser(self):
        self.client.logout()

        User.objects.create_superuser(username="TamerSUPER",
                                      password="pirata123"
                                      )

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_chepare_url)

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTrue(response.wsgi_request.user.is_superuser)

        self.assertTemplateUsed(response,
                                "delete-chepare.html"
                                )

        self.assertNotEqual(response.wsgi_request.user.username,
                            self.chepare.created_by.username
                            )

    def test_normal_logged_in_user_tries_to_reach_delete_chepare_item_which_is_created_by_another_user(self):
        User.objects.create_user(username="TamerTEST",
                                 password="pirata123"
                                 )
        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_chepare_url)

        self.assertTrue(response.status_code == 302)

        self.assertRedirects(response,
                             reverse("display_chepareta")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-chepare.html"
                                   )
