import re

from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


def validate_name(value):
    if value.count("_") > 1:
        raise ValidationError(
            "You can't use only underscores or have more than one underscore"
        )

    if not list(re.finditer(r'^\w+$', value)):
        raise ValidationError(
            "You can only use letters, numbers and underscores"
        )


class RedirectNotAuthorizedUsers(PermissionRequiredMixin, UserPassesTestMixin):
    user_must_be_logged = True
    no_permission_redirect_to = 'home'

    def test_func(self):
        user = self.request.user

        if self.user_must_be_logged and user.is_authenticated:
            if any(x == True for x in (user.is_superuser,
                                       self.check_obj_owner(user),
                                       user.has_perm(self.permission_required),
                                       )):
                return True

        return False

    def check_obj_owner(self, user):
        item = self.get_object()

        if hasattr(item, 'created_by'):
            return item.created_by.pk == user.pk

        return item.pk == user.pk

    def has_permission(self):
        user = self.request.user
        group_name = "staff"

        if user.pk == self.get_object().created_by.pk:
            return True

        if user.is_superuser:
            return True

        if super().has_permission():
            if user.groups.filter(name=group_name).exists():
                return True

        return False

    def handle_no_permission(self):
        return redirect(self.no_permission_redirect_to)


class RedirectNotAuthenticatedUsers(UserPassesTestMixin):
    redirect_to = "home"
    user_must_be_authenticated = True

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.redirect_to)
