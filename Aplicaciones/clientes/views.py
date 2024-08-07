from django.shortcuts import render, redirect,get_object_or_404
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
    dni = request.POST['txtDNI']
    celular_emergencia = request.POST['txtCelular']
    altura = request.POST['NumAltura']
    if altura == "":
        altura = None 
    else:
        altura = float(altura)
    
    peso = request.POST['NumPeso']
    if peso == "":
        peso = None
    else:
        peso = int(peso)
        
    obra_social = request.POST['txtObra']
    consideraciones = request.POST['txtConsideraciones']

    # Captura los valores de los checkboxes
    esguince = 'esguince' in request.POST
    fractura = 'fractura' in request.POST
    fisura = 'fisura' in request.POST
    protesis = 'protesis' in request.POST
    hernias = 'hernias' in request.POST
    desgarro = 'desgarro' in request.POST
    cirugias = 'cirugias' in request.POST
    tuvo_covid = 'tuvo_covid' in request.POST
    alguna_cardiopatia = 'alguna_cardiopatia' in request.POST
    tiroides = 'tiroides' in request.POST
    transplantes = 'transplantes' in request.POST
    hipertension = 'hipertension' in request.POST
    alzheimer = 'alzheimer' in request.POST
    asma = 'asma' in request.POST

    # Busca la instancia existente de FichaMedica
    fichamedica = get_object_or_404(FichaMedica, dni_id=dni)
    
    # Actualiza los campos de la instancia
    fichamedica.celular_emergencia = celular_emergencia
    fichamedica.altura = altura
    fichamedica.peso = peso
    fichamedica.obra_social = obra_social
    fichamedica.consideraciones = consideraciones
    
    # Actualiza los campos del cuestionario médico
    fichamedica.esguince = esguince
    fichamedica.fractura = fractura
    fichamedica.fisura = fisura
    fichamedica.protesis = protesis
    fichamedica.hernias = hernias
    fichamedica.desgarro = desgarro
    fichamedica.cirugias = cirugias
    fichamedica.tuvo_covid = tuvo_covid
    fichamedica.alguna_cardiopatia = alguna_cardiopatia
    fichamedica.tiroides = tiroides
    fichamedica.transplantes = transplantes
    fichamedica.hipertension = hipertension
    fichamedica.alzheimer = alzheimer
    fichamedica.asma = asma
    
    # Guarda la instancia actualizada
    fichamedica.save()
    
    return redirect('/')


def salir(request):
    logout(request)
    return redirect("/")

