from django.contrib import admin

from users.backends import User

# Register your models here.

admin.site.register(User)
