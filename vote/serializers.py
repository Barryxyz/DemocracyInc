from .models import VoteCount, VoteRecord
from rest_framework import serializers


class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount



class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteRecord

