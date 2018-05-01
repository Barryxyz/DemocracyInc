from .models import Election, Primary_VoteRecord, General_VoteRecord, VoteCount
from rest_framework import serializers

# used to access the database for external api to return types of elections available
class electionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='election_id')
    print("serializing election")
    class Meta:
        model = Election
        fields = ('id', 'type',)

# used to access the database for external api to return ballots of the primary election
class primarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Primary_VoteRecord
        fields = ('president_nominee',)

# used to access the database for external api to return the ballots of the general election
class generalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = General_VoteRecord
        # print("serializing general election")
        fields = ('president', 'vice_president', 'house_rep', 'senator',)

# used to access the database for external api to return the election result statistics
class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        fields = ('name', 'position', 'count',)

