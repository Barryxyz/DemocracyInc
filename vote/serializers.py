from .models import VoteCount, VoteRecord, Election
from rest_framework import serializers


class electionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Election
        # fields = '_all_' , not working for some reason...
        fields = ('id', 'type')


class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        # fields = '_all_' , not working for some reason...
        fields = ('name', 'position', 'count')



class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteRecord
        # fields = '__all__'
        fields = ('president', 'governor', 'lieutenant_Governor', 'attorney_General', 'delegate',
                  'commonwealth_Attorney', 'sheriff', 'treasurer')

