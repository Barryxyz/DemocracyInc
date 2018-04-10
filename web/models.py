from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import datetime


# Create your models here.

class Voter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(max_length=8, default=datetime.date.today)
    election_type = models.CharField(max_length=50, default='')
    locality = models.CharField(max_length=20, default = '')
    photo_id = models.CharField(max_length=20, default = '')
    confirmation = models.CharField(max_length=6)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'confirmation': self.confirmation,
            'id': self.id,
        }

    def __str__(self):
        return self.first_name

class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'id': self.id,
        }

class Vote(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)

    def to_json(self):
        return {
            'time_stamp': self.time_stamp,
            'voter': self.voter,
            'id': self.id,
        }

class Position(models.Model):
    name = models.CharField(max_length=50)

    def to_json(self):
        return {
            'name': self.name,
            'id': self.id,
        }
