#acá trabasformaremos los datos a json o desde json
#se necesita un modelo (models serializers)
#una url llama al view, y el view al modelo o serializador en este caso.
#view -> serializers -> transformación d edatos

from .models import Producto, Marca
from rest_framework import serializers


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

#customizar como quiero q se vean los datos en la api-rest
#validaciones para el form del testeo de apirest.
class ProductoSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.CharField(read_only=True, source="marca.nombre")
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all(), source="marca")
    nombre = serializers.CharField(required=True, min_length=3)

    #validacion si produycto ya existe dentro del form de api-rest
    def validate_nombre(self, value):
        existe = Producto.objects.filter(nombre__iexact=value).exists()

        if existe:
            raise serializers.ValidationError("Este producto ya existe")

        return value

    class Meta:
        model = Producto
        fields = '__all__'