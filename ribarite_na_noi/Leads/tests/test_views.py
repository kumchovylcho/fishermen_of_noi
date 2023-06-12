from django.contrib.auth.models import User
from django.test import (TestCase,
                         Client,
                         )
from django.urls import reverse

from ribarite_na_noi.Leads.models import Lead


class TestDisplayLeads(TestCase):

    def create_two_leads(self):
        lead_1 = Lead.objects.create(lead_type="Капка",
                                     grams="45",
                                     price=0.45,
                                     created_by=self.user
                                     )
        lead_2 = Lead.objects.create(lead_type="Круша",
                                     grams="55",
                                     price=0.55,
                                     created_by=self.user
                                     )

        return lead_1, lead_2

    def setUp(self):
        self.client = Client()
        self.display_leads_url = reverse('display_leads')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )

    def test_display_leads_page_with_no_leads(self):
        response = self.client.get(self.display_leads_url)

        self.assertTemplateUsed(response,
                                "display-leads.html"
                                )

        self.assertEqual(len(response.context.get("all_leads")),
                         0
                         )

    def test_display_leads_order_by_price_ascending(self):
        lead_1, lead_2 = self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"sort_by": "price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         lead_1.price
                         )

        self.assertEqual(queryset[1].price,
                         lead_2.price
                         )

    def test_display_leads_order_by_price_descending(self):
        lead_1, lead_2 = self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"sort_by": "-price"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].price,
                         lead_2.price
                         )

        self.assertEqual(queryset[1].price,
                         lead_1.price
                         )

    def test_display_leads_order_by_lead_type_ascending(self):
        lead_1, lead_2 = self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"sort_by": "lead_type"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].lead_type,
                         lead_1.lead_type
                         )

        self.assertEqual(queryset[1].lead_type,
                         lead_2.lead_type
                         )

    def test_display_leads_order_by_lead_type_descending(self):
        lead_1, lead_2 = self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"sort_by": "-lead_type"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].lead_type,
                         lead_2.lead_type
                         )

        self.assertEqual(queryset[1].lead_type,
                         lead_1.lead_type
                         )

    def test_display_leads_order_by_grams_ascending(self):
        lead_1, lead_2 = self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"sort_by": "grams"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].grams,
                         lead_1.grams
                         )

        self.assertEqual(queryset[1].grams,
                         lead_2.grams
                         )

    def test_display_leads_order_by_grams_descending(self):
        lead_1, lead_2 = self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"sort_by": "-grams"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset[0].grams,
                         lead_2.grams
                         )

        self.assertEqual(queryset[1].grams,
                         lead_1.grams
                         )

    def test_display_leads_filter_by_kapka(self):
        self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "Капка"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_krusha(self):
        self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "Круша"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_moliv(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.lead_type = "Молив"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "Молив"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_10(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.grams = "10"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "10"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_20(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.grams = "20"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "20"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_25(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.grams = "25"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "25"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_30(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.grams = "30"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "30"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_35(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.grams = "35"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "35"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_40(self):
        lead_1, lead_2 = self.create_two_leads()
        lead_1.grams = "40"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "40"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_45(self):
        self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "45"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_50(self):
        lead_1, _ = self.create_two_leads()
        lead_1.grams = "50"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "50"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_55(self):
        self.create_two_leads()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "55"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_60(self):
        lead_1, _ = self.create_two_leads()
        lead_1.grams = "60"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "60"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_65(self):
        lead_1, _ = self.create_two_leads()
        lead_1.grams = "65"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "65"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )

    def test_display_leads_filter_by_grams_70(self):
        lead_1, _ = self.create_two_leads()
        lead_1.grams = "70"

        lead_1.save()

        response = self.client.get(self.display_leads_url,
                                   {"filter_by": "70"}
                                   )

        self.assertEqual(response.status_code,
                         200
                         )

        queryset = response.context.get("object_list")

        self.assertEqual(queryset.count(),
                         1
                         )


class TestCreateLead(TestCase):

    def create_lead_obj(self):
        lead_info = dict(lead_type="Капка",
                         grams="45",
                         price=0.45,
                         created_by=self.user
                         )

        return lead_info

    def setUp(self):
        self.client = Client()
        self.create_lead_url = reverse('create_lead')

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

    def test_successfully_create_lead(self):
        lead_data = self.create_lead_obj()

        response = self.client.post(self.create_lead_url,
                                    data=lead_data
                                    )

        lead = Lead.objects.get(grams="45")
        lead.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_leads')
                             )

        self.assertEqual("45",
                         lead.grams
                         )

    def test_user_tries_to_reach_create_lead_page_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.create_lead_url)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response,
                             reverse('display_leads')
                             )

        self.assertTemplateNotUsed(response,
                                   "create-lead.html"
                                   )


class TestEditLead(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.lead = Lead.objects.create(lead_type="Капка",
                                        grams="45",
                                        price=0.45,
                                        created_by=self.user
                                        )

        self.edit_lead_url = reverse('edit_lead',
                                     kwargs={'pk': self.lead.pk}
                                     )

    def test_successfully_edit_lead_which_is_created_by_the_user(self):
        data_entered = dict(lead_type="Капка",
                            grams="55",
                            price=0.45,
                            created_by=self.user
                            )

        response = self.client.post(self.edit_lead_url,
                                    data=data_entered
                                    )

        self.lead.refresh_from_db()

        self.assertRedirects(response,
                             reverse('display_leads')
                             )

        self.assertEqual(self.lead.grams,
                         "55"
                         )

        self.assertFalse(self.lead.price == 1000)

    def test_user_tries_to_land_on_edit_lead_item_page_which_is_not_created_by_him(self):
        user_2 = User.objects.create_user(username="TamerTEST",
                                          password="pirata123"
                                          )

        self.client.logout()

        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_lead_url)

        self.assertRedirects(response,
                             reverse('display_leads')
                             )

        self.assertNotEqual(self.lead.created_by.pk,
                            user_2.pk
                            )

        self.assertTemplateNotUsed(response,
                                   "edit-lead.html"
                                   )

    def test_superuser_tries_to_land_on_edit_lead_item_page_which_is_not_created_by_him(self):
        superuser = User.objects.create_superuser(username="TamerSUPER",
                                                  password="pirata123"
                                                  )
        self.client.logout()

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.edit_lead_url)

        self.assertNotEqual(self.lead.created_by.pk,
                            superuser.pk
                            )

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTemplateUsed(response,
                                "edit-lead.html"
                                )

    def test_not_logged_in_user_tries_to_land_on_edit_item_page(self):
        self.client.logout()

        response = self.client.get(self.edit_lead_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse('display_leads')
                             )

        self.assertTemplateNotUsed(response,
                                   "edit-lead.html"
                                   )


class TestDeleteLead(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="Tamer",
                                             password="pirata123"
                                             )
        self.client.login(username="Tamer",
                          password="pirata123"
                          )

        self.lead = Lead.objects.create(lead_type="Капка",
                                        grams="55",
                                        price=0.45,
                                        created_by=self.user
                                        )

        self.delete_lead_url = reverse('delete_lead',
                                       kwargs={'pk': self.lead.pk}
                                       )

    def test_successfully_delete_lead_which_is_created_by_the_user(self):
        response = self.client.post(self.delete_lead_url)

        self.assertEqual(Lead.objects.filter(lead_type="Капка").count(),
                         0
                         )

        self.assertRedirects(response,
                             reverse("display_leads")
                             )

    def test_not_logged_in_user_tries_to_reach_delete_lead_url(self):
        self.client.logout()

        response = self.client.get(self.delete_lead_url)

        self.assertEqual(response.status_code,
                         302
                         )

        self.assertRedirects(response,
                             reverse("display_leads")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-lead.html"
                                   )

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_superuser_tries_to_reach_delete_lead_url_which_is_not_created_by_the_superuser(self):
        self.client.logout()

        User.objects.create_superuser(username="TamerSUPER",
                                      password="pirata123"
                                      )

        self.client.login(username="TamerSUPER",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_lead_url)

        self.assertEqual(response.status_code,
                         200
                         )

        self.assertTrue(response.wsgi_request.user.is_superuser)

        self.assertTemplateUsed(response,
                                "delete-lead.html"
                                )

        self.assertNotEqual(response.wsgi_request.user.username,
                            self.lead.created_by.username
                            )

    def test_normal_logged_in_user_tries_to_reach_lead_which_is_created_by_another_user(self):
        User.objects.create_user(username="TamerTEST",
                                 password="pirata123"
                                 )
        self.client.login(username="TamerTEST",
                          password="pirata123"
                          )

        response = self.client.get(self.delete_lead_url)

        self.assertTrue(response.status_code == 302)

        self.assertRedirects(response,
                             reverse("display_leads")
                             )

        self.assertTemplateNotUsed(response,
                                   "delete-lead.html"
                                   )
