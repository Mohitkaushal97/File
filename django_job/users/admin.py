# from allauth.account.models import EmailAddress
# from django.contrib import admin
# from django.contrib.auth import admin as auth_admin
# from django.contrib.auth import get_user_model
# from django_job.users.forms import UserCreationForm, UserChangeForm
#
# User = get_user_model()
#
# class EmailAddressInline(admin.TabularInline):
#     model = EmailAddress
#     extra = 1
#     exclude = ('primary',)
#
# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#     inlines = (EmailAddressInline,)
#
#     form = UserChangeForm
#     add_form = UserCreationForm
#     fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
#     list_display = ["username", "name", "is_superuser"]
#     search_fields = ["name"]
#
# # @admin.register(User)
# # class UserAdmin(nested_admin.UserAdmin):
# #     inlines = (EmailAddressInline,)
