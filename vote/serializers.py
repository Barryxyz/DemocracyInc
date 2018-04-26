from .models import VoteCount, VoteRecord
from rest_framework import serializers


class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        # fields = '_all_'
        fields = ('name', 'position', 'count')



class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteRecord
        fields = '_all_'

