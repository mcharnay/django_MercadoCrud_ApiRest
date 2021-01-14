from django import forms
from .models import Contacto, Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import MaxSizeFileValidator #import de validators.py
from django.forms import ValidationError


#este formulario hay que importarlo a las vistas.
class ContactoForm(forms.ModelForm):

    #nombre = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    #meta toma los campos del html
    class Meta:
        model = Contacto
        #fields = ["nombre", "correo", "tipo_consulta", "mensaje", "avisos"]
        fields= '__all__'


class ProductoForm(forms.ModelForm):

    #validaciones

    #min y max de caracteres
    nombre = forms.CharField(min_length=3, max_length=50)

    #para no requerir la imagen, igual en el modelo la imagen de null debe estar en true.
    imagen = forms.ImageField(required=False, validators=[MaxSizeFileValidator(max_file_size=1)])

    #validacion precio entre 1 y 1500000
    precio = forms.IntegerField(min_value=1, max_value=1500000)

    #validación cosa que el nombre del producto no se repita.
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()

        if existe:
            raise ValidationError("Este nombre ya existe")
        
        return nombre

    class Meta:
        model = Producto
        fields = '__all__'

        #para mostrar fecha en formulario
        widgets = {
            "fecha_fabricacion": forms.SelectDateWidget()
        }


#importarlo en view, este es el form de crear usuario con los datos que yo quiero crear
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

