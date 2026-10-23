import math
from rest_framework import serializers
from .models import Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=['id','number','title','concept']
class ConversionInput(serializers.Serializer):
    celsius=serializers.FloatField(min_value=-273.15,max_value=10000)
    def validate_celsius(self,value):
        if not math.isfinite(value):raise serializers.ValidationError('Valor finito requerido.')
        return value
