from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registerValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['firstname']) < 2:
            errors['fname'] = "First name is required to be at least 2 characters!"
        if len(postData['lastname']) < 2:
            errors['lname'] = "Last name is required to be at least 2 characters!"
        if len(postData['email']) == 0:
            errors['emailrequired'] = "Email is required!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalidemail'] = "Email not valid!"
        if len(postData['pw']) < 8:
            errors['pw_length'] = "Password should be at least 8 characters!"
        if postData['pw'] != postData['confirm']:
            errors['nomatch'] = "Password does not match!"

        return errors

    def loginValidator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['emailrequired'] = "Email required"
        else:
            usersWithEmail = User.objects.filter(email = postData['email'])
            print(usersWithEmail)
            if len(usersWithEmail)==0:
                errors['emailnotregistered'] = "Email not found, please register."
            else:
                usertocheck = usersWithEmail[0]
                if bcrypt.checkpw(postData['pw'].encode(),usertocheck.password.encode()):
                    print('password match')
                else:
                    errors['pwwrong'] = "Password incorrect."
        return errors

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# Create your models here.
