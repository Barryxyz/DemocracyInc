from .models import Election, VoteRecord, VoteCount
from rest_framework import serializers

# used to access the database for external api to return types of elections available
class electionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='election_id')
    class Meta:
        model = Election
        fields = ('id', 'type',)

# used to access the database for external api to return ballots of the primary election
class voteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteRecord
        fields = ('position','candidate')

# used to access the database for external api to return the election result statistics
class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        fields = ('name', 'position', 'count',)

