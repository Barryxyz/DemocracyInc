# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Election(models.Model):
    election_id = models.CharField(max_length=7, default=None, null=True)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='inactive')

    def to_json(self):
        return {
            'id': self.election_id,
            'type': self.type
        }

    def __str__(self):
        return self.election_id, self.type

class Position(models.Model):
    name = models.CharField(max_length=50)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=None)

class Candidate(models.Model):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=None)

class Voter(models.Model):
    voter_number = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    voter_status = models.CharField(max_length=20, null=True)
    date_registered = models.DateField(max_length=8, default=datetime.date.today)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=2, null=True)
    zip = models.DecimalField(max_digits=5, decimal_places=0)
    locality = models.CharField(max_length=20, null=True)
    precinct = models.CharField(max_length=100, null=True)
    precinct_id = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    confirmation = models.CharField(max_length=6, null=True)
    checkin_time_stamp = models.DateTimeField(null=True)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'confirmation': self.confirmation,
            'id': self.id,
        }

    def __str__(self):
        return self.first_name

class VoteCount(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    count = models.CharField(max_length=50)
    election = models.CharField(max_length=50, null=True)

    def to_json(self):
        return {
            'name': self.name,
            'position': self.position,
            'count': self.count,
            'election': self.election
        }

    def __str__(self):
        return self.name, self.position, self.count

class PollWorker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    precinct_id = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    locality = models.CharField(max_length=20, null=True)

class General_VoteRecord(models.Model):
    president = models.CharField(max_length=100)
    vice_president = models.CharField(max_length=100)
    house_rep = models.CharField(max_length=100)
    senator = models.CharField(max_length=100)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, default=None)
    time_stamp = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
            'president': self.president,
            'vice_president': self.vice_president,
            'house_rep': self.house_rep,
            'senator': self.senator,
            'voter': self.voter,
            'time_stamp': self.time_stamp,
        }

    def __str__(self):
        return self.president, self.vice_president, self.house_rep, self.senator, self.voter, self.time_stamp

class Primary_VoteRecord(models.Model):
    president_nominee = models.CharField(max_length=100)
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE, default=None)
    time_stamp = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
            'president_nominee': self.president_nominee,
            'voter': self.voter,
            'time_stamp': self.time_stamp,
        }

    def __str__(self):
        return self.president_nominee, self.voter, self.time_stamp