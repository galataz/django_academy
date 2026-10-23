from rest_framework.views import APIView
from rest_framework.response import Response
from academy.serializers import ConversionInput
from UTIL_LIB.conversiones import celsius_a_fahrenheit
class ConvertTemperatureCommand(APIView):
    """Operación de laboratorio sin persistencia ni identidad."""
    def post(self,request):
        serializer=ConversionInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        value=serializer.validated_data['celsius']
        return Response({'success':True,'celsius':value,'fahrenheit':celsius_a_fahrenheit(value)})
