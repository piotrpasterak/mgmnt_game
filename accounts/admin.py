from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .form import UserCreateForm

class MyUserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'gender', 'experience', 'password1', 'password2')}
        ),
    )
    list_display = ('username', 'is_superuser','email', 'is_staff', 'gender', 'experience')


admin.site.register(CustomUser, MyUserAdmin)
