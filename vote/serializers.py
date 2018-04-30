from .models import Election, Primary_VoteRecord, General_VoteRecord, VoteCount, VoteRecord
from rest_framework import serializers


class electionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='election_id')
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
        # fields = '__all__'
        fields = ('president', 'vice_president', 'house_rep', 'senator',)


class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteCount
        # fields = '_all_' , not working for some reason...
        fields = ('name', 'position', 'count',)

#
#
# class RecordSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = VoteRecord
#         # fields = '__all__'
#         fields = ('president', 'governor', 'lieutenant_Governor', 'attorney_General', 'delegate',
#                   'commonwealth_Attorney', 'sheriff', 'treasurer')
#

class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteRecord
        # fields = '__all__'
        fields = ('president', 'governor', 'lieutenant_Governor', 'attorney_General', 'delegate',
                  'commonwealth_Attorney', 'sheriff', 'treasurer',)
