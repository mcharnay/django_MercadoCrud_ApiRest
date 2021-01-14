from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm #import de contactoForm en forms.py
from django.contrib import messages #import de framwork de MESSAGE_STORAGE en settings
from django.core.paginator import Paginator #import clase para paginar resultado de búsqyedas 
from django.http import Http404 #import para el paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets #import para el rest
from .serializers import ProductoSerializer #import de serializers

# Create your views here.


#clase para usar el rest.
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer #importarlo en urls

    def get_queryset(self):
        productos = Producto.objects.all()

        nombre = self.request.GET.get('nombre')

        if nombre:
            productos = productos.filter(nombre__contains=nombre)#contains es como like, para que salgan coincidencias.
            #así se busca: 127.0.0.1:8000/api/producto/?nombre=lava&tele

        return productos




#Las vistas serán llamadas desde el urls.py que se cre+o dentro del módulo de nuestra app, no desde la original del proyecto

#se envía la vista, y de paso un select all de los productos a la vista home.
def home(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/home.html', data)


#trae tambiuén el formulario de forms.py
#se imorta el forms.py, y se envía a app/contacto.html
def contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto Guardado"
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html', data)

#@login_required
def galeria(request):
    return render(request, 'app/galeria.html')

@permission_required('app.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
            return redirect(to="listar_productos")
        else:
            data["form"]= formulario
    return render(request, 'app/producto/agregar.html', data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all() #trae select all de productos

    #paginar lista
    page = request.GET.get('page', 1)  #recoger num de páginas desde la url 

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page) # trae el page de arriba.
    except:
        raise Http404

    data = {
        'entity': productos, #ahora se llama entity, y se recorre en listar.html por entity y no productos.
        'paginator': paginator
    }

    return render(request, 'app/producto/listar.html', data)

@permission_required('app.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente") #nessage de MESSAGE_STORAGE, se envía a base.html
            return redirect(to="listar_productos")
        data["form"] = formulario

    return render(request, 'app/producto/modificar.html', data)

@permission_required('app.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correcto")
    return redirect(to="listar_productos")


#la data proviene del forms.py
def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)
