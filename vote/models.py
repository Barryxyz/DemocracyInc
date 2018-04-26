# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils.timezone import now

Locality = (
    ('001', 'Accomack'),
    ('003', 'Albemarle'),
    ('005', 'Alleghany'),
    ('007', 'Amelia'),
    ('009', 'Amherst'),
    ('011', 'Appomattox'),
    ('013', 'Arlington'),
    ('015', 'Augusta'),
    ('017', 'Bath'),
    ('019', 'Bedford'),
    ('021', 'Bland'),
    ('023', 'Botetourt'),
    ('025', 'Brunswick'),
    ('027', 'Buchanan'),
    ('029', 'Buckingham'),
    ('031', 'Campbell'),
    ('033', 'Caroline'),
    ('035', 'Carroll'),
    ('036', 'Charles City'),
    ('037', 'Charlotte'),
    ('041', 'Chesterfield'),
    ('043', 'Clarke'),
    ('045', 'Craig'),
    ('047', 'Culpeper'),
    ('049', 'Cumberland'),
    ('051', 'Dickenson'),
    ('053', 'Dinwiddie'),
    ('057', 'Essex'),
    ('059', 'Fairfax'),
    ('061', 'Fauquier'),
    ('063', 'Floyd'),
    ('065', 'Flunna'),
    ('067', 'Franklin'),
    ('069', 'Frederick'),
    ('071', 'Giles'),
    ('073', 'Gloucester'),
    ('075', 'Goochland'),
    ('077', 'Grayson'),
    ('079', 'Greene'),
    ('081', 'Greensville'),
    ('083', 'Halifax'),
    ('085', 'Hanover'),
    ('087', 'Henrico'),
    ('089', 'Henry'),
    ('091', 'Highland'),
    ('093', 'Isle of Wight'),
    ('095', 'James City'),
    ('097', 'King and Queen'),
    ('099', 'King George'),
    ('101', 'King William'),
    ('103', 'Lancaster'),
    ('105', 'Lee'),
    ('107', 'Loudoun'),
    ('109', 'Louisa'),
    ('111', 'Lunenburg'),
    ('113', 'Madison'),
    ('115', 'Mathews'),
    ('117', 'Mecklenburg'),
    ('119', 'Middlesex'),
    ('121', 'Montgomery'),
    ('125', 'Nelson'),
    ('127', 'New Kent'),
    ('131', 'Northampton'),
    ('133', 'Northumberland'),
    ('135', 'Nottoway'),
    ('137', 'Orange'),
    ('139', 'Page'),
    ('141', 'Patrick'),
    ('143', 'Pittsylnia'),
    ('145', 'Powhatan'),
    ('147', 'Prince Edward'),
    ('149', 'Prince George'),
    ('153', 'Prince William'),
    ('155', 'Pulaski'),
    ('157', 'Rappahannock'),
    ('159', 'Richmond'),
    ('161', 'Roanoke'),
    ('163', 'Rockbridge'),
    ('165', 'Rockingham'),
    ('167', 'Russell'),
    ('169', 'Scott'),
    ('171', 'Shenandoah'),
    ('173', 'Smyth'),
    ('175', 'Southampton'),
    ('177', 'Spotsylnia'),
    ('179', 'Stafford'),
    ('181', 'Surry'),
    ('183', 'Sussex'),
    ('185', 'Tazewell'),
    ('187', 'Warren'),
    ('191', 'Washington'),
    ('193', 'Westmoreland'),
    ('195', 'Wise'),
    ('197', 'Wythe'),
    ('199', 'York'),
    ('510', 'Alexandria City'),
    ('515', 'Bedford City'),
    ('520', 'Bristol City'),
    ('530', 'Buena Vista City'),
    ('540', 'Charlottesville City'),
    ('550', 'Chesapeake City'),
    ('560', 'Clifton Forge City'),
    ('570', 'Colonial Heights City'),
    ('580', 'Covington City'),
    ('590', 'Danville City'),
    ('595', 'Emporia City'),
    ('600', 'Fairfax City'),
    ('610', 'Falls Church City'),
    ('620', 'Franklin City'),
    ('630', 'Fredericksburg City'),
    ('640', 'Galax City'),
    ('650', 'Hampton City'),
    ('660', 'Harrisonburg City'),
    ('670', 'Hopewell City'),
    ('678', 'Lexington City'),
    ('680', 'Lynchburg City'),
    ('683', 'Manassas City'),
    ('685', 'Manassas Park City'),
    ('690', 'Martinsville City'),
    ('700', 'Newport News City'),
    ('710', 'Norfolk City'),
    ('720', 'Norton City'),
    ('730', 'Petersburg City'),
    ('735', 'Poquoson City'),
    ('740', 'Portsmouth City'),
    ('750', 'Radford City'),
    ('760', 'Richmond City'),
    ('770', 'Roanoke City'),
    ('775', 'Salem City'),
    ('780', 'South Boston City'),
    ('790', 'Staunton City'),
    ('800', 'Suffolk City'),
    ('810', 'Virginia Beach City'),
    ('820', 'Waynesboro City'),
    ('830', 'Williamsburg City'),
    ('840', 'Winchester City')
)

President = (
    ('Hillary Clinton', 'Hillary Clinton - (D)'),
    ('Donald Trump', 'Donald Trump - (R)'),
    ('Gary Johnson', 'Gary Johnson - (L)')
)

Governor = (
    ('Matthew Ray', 'Matthew Ray - (D)'),
    ('Marisha Miller', 'Marisha Miller - (R)'),
    ('Travis Bailey', 'Travis Bailey - (L)')
)

LieuGov = (
    ('Laura Willingham', 'Laura Willingham - (D)'),
    ('Samuel Brien', 'Samuel Brien - (R)')
)

AttGen = (
    ('Liam Riegel', 'Liam Riegel - (D)'),
    ('Allison Haffe', 'Allison Haffe - (R)')
)

Delegate = (
    ('Brian W. Johnson', 'Brian W. Johnson - (D)'),
    ('Joe Hardwick', 'Joe Hardwick - (R)')
)

CommAtt = (
    ('Ashley Foster', 'Ashley Foster'),
    ('Chris Manganiello', 'Chris Manganiello')
)

Sheriff = (
    ('Mary Friedle', 'Mary Friedle'),
    ('Will McGlynn', 'Will McGlynn'),
    ('Wil Day', 'Wil Day')
)

Treasurer = (
    ('Felicia Wheaton', 'Felicia Wheaton'),
    ('Patrick Charles', 'Patrick Charles'),
    ('Jason Rothfuss', 'Jason Rothfuss')
)

class Election(models.Model):
    election_id = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type
        }


    def __str__(self):
        return self.type



class VoteCount(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    count = models.CharField(max_length=50)

    def to_json(self):
        return {
            'name': self.name,
            'position': self.position,
            'count': self.count,
        }

    def __str__(self):
        return self.name, self.position, self.count



class Voter(models.Model):
    # voter_number = models.IntegerField(max_length=12)
    # voter_status = models.CharField(max_length=20)
    # date_registered = models.DateField(max_length=8, default=datetime.date.today)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=8, default=datetime.date.today)
    # might not even be included with api json... ^^
    # election_type = models.CharField(max_length=50, default='')
    # state = models.CharField(max_length=2)
    # zip = models.IntegerField(max_length=5)
    locality = models.CharField(max_length=20, default='')
    # precinct = models.CharField(max_length=20, default='')
    # precinct_id = models.IntegerField(max_length=10)
    confirmation = models.CharField(max_length=6)
    #voter_id = models.CharField(max_length=6)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'confirmation': self.confirmation,
            #'voter_id': self.voter_id,
            'id': self.id,
        }

    def __str__(self):
        return self.first_name

class PollPlace(models.Model):
    precinct = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    poll_booths = models.IntegerField()

class VoteRecord(models.Model):
    president = models.CharField(max_length=50, choices=President)
    governor = models.CharField(max_length=50, choices=Governor)
    lieutenant_Governor = models.CharField(max_length=50, choices=LieuGov)
    attorney_General = models.CharField(max_length=50, choices=AttGen)
    delegate = models.CharField(max_length=50, choices=Delegate)
    commonwealth_Attorney = models.CharField(max_length=50, choices=CommAtt)
    sheriff = models.CharField(max_length=50, choices=Sheriff)
    treasurer = models.CharField(max_length=50, choices=Treasurer)
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE, default='')
    time_stamp = models.DateTimeField(auto_now=True)


    def to_json(self):
        return {
            'president': self.president,
            'governor': self.governor,
            'lieutenant_Governor': self.lieutenant_Governor,
            'attorney_General': self.attorney_General,
            'first_name': self.delegate,
            'commonwealth_Attorney': self.commonwealth_Attorney,
            'sheriff': self.sheriff,
            'treasurer': self.treasurer,
            'voter': self.voter,
            'time_stamp': self.time_stamp,
        }

    def __str__(self):
        return self.president, self.governor, self.lieutenant_Governor, self.attorney_General, self.delegate, \
               self.commonwealth_Attorney, self.sheriff, self.treasurer, self.voter, self.time_stamp