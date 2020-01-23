from django.db import models
from django.contrib.auth.hashers import check_password as ckpass,\
    make_password as mkpass, is_password_usable as ispassuse


class User(models.Model):
    nick = models.CharField(max_length=127)
    password = models.CharField(max_length=127)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=7)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.nick

    # password
    def set_password(self, new_password):
        self.password = mkpass(new_password)
        self.save()
        return

    def check_password(self, password):
        if ispassuse(password):
            # will work only with the same salt!
            return password == self.password
        return ckpass(password, self.password)