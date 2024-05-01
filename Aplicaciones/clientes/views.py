from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente, FichaMedica
from django.utils import timezone
from datetime import datetime ,timedelta
from django.contrib.auth import logout

# Create your views here.

@login_required
def home(request):
    clientes= Cliente.objects.all()
    
    dniError=False
    # Obtener la fecha actual
    fecha_actual = timezone.now().date()
    fecha_un_dia_antes = fecha_actual - timedelta(days=1)
    

    # Obtener todos los clientes cuya fecha de alta sea mayor o igual a la fecha actual
    clientes_activos = Cliente.objects.filter(fecha_baja__gte=fecha_actual)
    clientes_inactivos=Cliente.objects.filter(fecha_baja__lte=fecha_un_dia_antes)
    try:
        if request.session.get("dniError")==True:
            dniError=True
    except:
        pass
    request.session["dniError"]=False
    return render(request,"gestionClientes.html",{"clientes":clientes,"dniError":dniError, "clientes_activos":clientes_activos,"clientes_inactivos":clientes_inactivos})
@login_required
def registrarCliente(request):
    fecha_actual = datetime.now().date()

    # Sumarle 30 días
    fecha_en_30_dias = fecha_actual + timedelta(days=30)
    dni=request.POST['txtDNI']
    nombre=request.POST['txtNombre']
    apellido=request.POST['txtApellido']
    nacimiento=request.POST['dateNacimiento']
    request.session["dniError"]=False
    try:
        cliente = Cliente.objects.create(dni=dni, nombre=nombre, apellido=apellido, nacimiento=nacimiento,fecha_baja=fecha_en_30_dias)
        
        FichaMedica.objects.create(dni_id=dni)   
        
    except:
        try:
            request.session["dniError"]=True
        except:
            print("no funciono")
        print("paso por aca")
    
    return redirect('/')
@login_required
def eliminacionCliente(request, dni):
    
    fecha_actual = datetime.now().date()

# Restarle un día
    fecha_un_dia_antes = fecha_actual - timedelta(days=1)
    # Si solo necesitas la fecha en formato de cadena, puedes usar strftime
    fecha_actual_str = fecha_un_dia_antes.strftime("%Y-%m-%d")
    cliente=Cliente.objects.get(dni=dni)
    cliente.fecha_baja=fecha_actual_str
    cliente.save()
    return redirect ("/")

@login_required
def activarCliente(request,dni):
    fecha_actual = datetime.now().date()

    # Sumarle 30 días
    fecha_en_30_dias = fecha_actual + timedelta(days=30)
    cliente=Cliente.objects.get(dni=dni)
    cliente.fecha_baja=fecha_en_30_dias
    
    cliente.save()
    return redirect ("/")
@login_required
def edicionCliente(request, dni):
    cliente=Cliente.objects.get(dni=dni)
    
    nacimiento=str(cliente.nacimiento)
    return render(request,"edicionCliente.html",{'Cliente':cliente, 'nacimiento':nacimiento})
@login_required
def editarCliente(request):
    dni=request.POST['txtDNI']
    Nombre=request.POST['txtNombre']
    Apellido=request.POST['txtApellido']
    Nacimiento=request.POST['dateNacimiento']
    
    cliente=Cliente.objects.get(dni=dni)
    cliente.nombre=Nombre
    cliente.apellido=Apellido
    cliente.nacimiento=Nacimiento
    cliente.save()
    
    return redirect('/')
@login_required
def verFichaMedica(request, dni):
    cliente=FichaMedica.objects.get(dni=dni)
    
    return render(request,"fichaMedica.html",{'cliente':cliente})
@login_required
def editarFichaMedica(request):
    dni=request.POST['txtDNI']
    celular_emergencia=request.POST['txtCelular']
    altura=request.POST['NumAltura']
    if altura == "" :
        altura=None 
    else:
        altura=float(altura)
    
    peso=request.POST['NumPeso']
    if peso == "" :
        peso=None
    else:
        peso=int(peso)
    obra_social=request.POST['txtObra']
    consideraciones=request.POST['txtConsideraciones']
    fichamedica=FichaMedica.objects.get(dni_id=dni)
    fichamedica.delete()
    fichamedica=FichaMedica.objects.create(dni_id=dni,celular_emergencia=celular_emergencia,altura=altura,
                                           peso=peso,obra_social=obra_social,consideraciones=consideraciones)
    return redirect('/')


def salir(request):
    logout(request)
    return redirect("/")

