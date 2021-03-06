from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['fname']="First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['lname']="Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="Please enter a valid email"
        if not PASS_REGEX.match(postData['pass']):
            errors['pass']="Password must be between 8 and 20 characters \
                and contain one uppercase letter, one lowercase letter \
                    and one number"
        if postData['pass'] != postData['cpass']:
            errors['cpass'] = "Passwords must match"
        return errors

    def login_validator(self, postData):
        login_errors = {}
        user = User.objects.filter(email = postData['email'])
        if not user:
            login_errors['mail']="Please enter a valid email and password"
        elif not bcrypt.checkpw(postData['pass'].encode(), user[0].password.encode()):
            login_errors['mail']="Please enter a valid email and password"
        return login_errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
