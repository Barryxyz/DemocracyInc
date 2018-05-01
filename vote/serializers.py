from vote import models
from rest_framework import serializers

# used to access the database for external api to return types of elections available
class electionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='election_id')
    class Meta:
        model = models.Election
        fields = ('id', 'type',)

# used to access the database for external api to return ballots of the primary election
class voteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VoteRecord
        fields = "__all__"

# used to access the database for external api to return the election result statistics
class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VoteCount
        fields = ('name', 'position', 'count',)

