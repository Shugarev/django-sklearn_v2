from rest_framework import serializers
from rest_framework.fields import IntegerField

from datalab.models import DataSet


class DataSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataSet
        fields = '__all__'
