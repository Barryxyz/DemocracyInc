from .models import VoteCount, VoteRecord
from rest_framework import serializers


class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        fields = ('name', 'position', 'count')


class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteRecord
        fields = ('president', 'governor', 'lieutenant_Governor', 'attorney_General', 'delegate',
                  'commonwealth_Attorney', 'sheriff', 'treasurer', 'voter', 'time_stamp')
