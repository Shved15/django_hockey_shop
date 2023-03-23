from django.contrib import admin

from users.models import User
from products.admin import BagAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BagAdmin,)
