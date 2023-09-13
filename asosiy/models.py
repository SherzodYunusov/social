from django.db import models


class Kod(models.Model):
    kod = models.IntegerField()
    tel = models.CharField(max_length=1)
    def __str__(self):
        return self.tel

class Register(models.Model):
    TANLOV_CHOICES = [
        ('salom', 'Salom'),
        ('dunyo', 'dunyo')
    ]
    username = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)  # OneToOneField ishlatamiz
    category = models.CharField(max_length=100, choices=TANLOV_CHOICES)
    def __str__(self):
        return self.username


class Login(models.Model):
    phone_number = models.ForeignKey(Register, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class Password(models.Model):
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.password

class Programs(models.Model):
    name = models.CharField(max_length=100)
    package_name = models.CharField(max_length=100)
    enable = models.BooleanField(default=False)
    programs_id = models.ForeignKey(Password, on_delete=models.CASCADE, related_name='apps')

    def __str__(self):
        return self.name
# Create your models here.
