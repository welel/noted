from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User, SignupToken


admin.site.register(User, UserAdmin)
admin.site.register(SignupToken, admin.ModelAdmin)
