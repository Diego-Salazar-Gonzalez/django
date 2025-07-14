from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegistroClienteForm, LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from .models import Producto, Categoria
from .models import Producto
from collections import defaultdict
from django.db.utils import OperationalError
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
def inicio(request):
    try:
        productos = Producto.objects.select_related('categoria').all()
    except OperationalError:
        productos = []

    categorias_con_productos = defaultdict(list)
    print(productos)

    for p in productos:
        print(p)
        if p.imagen:
            imagen = p.imagen.url 
        else:
            imagen = '/static/img/placeholder.png'

        categorias_con_productos[p.categoria.nombre].append({
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio': str(p.precio),
            'imagen': imagen
        })

    return render(request, 'index.html', {
        'categorias_con_productos': dict(categorias_con_productos)
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = RegistroClienteForm()

    return render(request, 'registro.html', {'form': form})

def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('inicio')  # o donde desees
            else:
                form.add_error(None, "Credenciales inválidas")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def admin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print("Este usuario es superusuario")
        else:
            print("Usuario normal")
    print(request.user)
    return render(request,'admin.html')
def vista_productos(request):
    categorias = Categoria.objects.all()
    print(categorias)
def productos_por_categoria(request, categoria_id):
    try:
        productos = Producto.objects.filter(categoria_id=categoria_id)
        categoria = Categoria.objects.get(id=categoria_id)
    except OperationalError:
        productos = []
        categoria = None

    return render(request, 'productos.html', {
        'categorias': productos,
        'titulo_categoria': categoria.nombre if categoria else "Sin categoría"
    })


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener el carrito desde la sesión, o crear uno nuevo si no existe
    carrito = request.session.get('carrito', {})

    # Agregar el producto al carrito (por ahora sin cantidad, solo una vez)
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1  # suma cantidad
    else:
        carrito[str(producto_id)] = 1  # lo agrega con cantidad 1

    request.session['carrito'] = carrito  # Guardar carrito en sesión
    request.session.modified = True       # Marcar sesión como modificada

    return redirect('carrito')  # Redirigir a la vista del carrito

def carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())

    # Armar los datos para la plantilla
    carrito_detalles = []
    total = 0
    for producto in productos:
        cantidad = carrito.get(str(producto.id), 0)
        subtotal = producto.precio * cantidad
        total += subtotal
        carrito_detalles.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'carrito.html', {
        'carrito': carrito_detalles,
        'total': total,
    })
def pagar_carrito(request):
    # Aquí podrías procesar el pago real...
    request.session['carrito'] = {}  # Vaciar el carrito
    request.session.modified = True
    messages.success(request, "¡Gracias por tu compra!")
    return redirect('carrito')  # Redirige a la misma página del carrito
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')  
