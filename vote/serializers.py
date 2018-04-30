from .models import Election, Primary_VoteRecord, General_VoteRecord, VoteCount
from rest_framework import serializers


class electionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='election_id')
    print("serializing election")
    class Meta:
        model = Election
        # fields = '__all__'
        fields = ('id', 'type',)

class primarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Primary_VoteRecord
        # fields = '_all_' , not working for some reason...
        fields = ('president_nominee',)


class generalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = General_VoteRecord
        print("serializing general election")
        # fields = '__all__'
        fields = ('president', 'vice_president', 'house_rep', 'senator',)


class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        # fields = '_all_' , not working for some reason...
        fields = ('name', 'position', 'count',)

