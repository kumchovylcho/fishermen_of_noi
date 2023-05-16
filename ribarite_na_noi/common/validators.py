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