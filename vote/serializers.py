from vote import models
from rest_framework import serializers

# used to access the database for external api to return types of elections available
class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Election
        fields = ('election_id', 'type',)

# used to access the database for external api to return ballots of the active election
class VoteCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VoteCount
        fields = ('position', 'candidate','count')
