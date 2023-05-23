import re

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


def validate_name(value):
    if not bool(re.finditer(r'^\w+$', value)):
        raise ValidationError(
            "You can only use letters, numbers and underscores"
        )


class RedirectNotLoggedUsers(UserPassesTestMixin):
    user_must_be_logged = True
    no_permission_redirect_to = 'home'

    def test_func(self):
        if self.user_must_be_logged:
            return self.request.user.is_authenticated
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.no_permission_redirect_to)


class RedirectLoggedUsersUrlTypers(RedirectNotLoggedUsers):

    def test_func(self):
        is_authenticated = super().test_func()

        item = self.get_object()

        if self.request.user.is_superuser:
            return True

        if self.request.user.groups.filter(name="staff").exists():
            return True

        if hasattr(item, 'created_by'):
            return item.created_by.pk == self.request.user.pk and is_authenticated

        return item.pk == self.request.user.pk and is_authenticated
