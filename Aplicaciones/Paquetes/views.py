from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Paquete
from django.utils import timezone
# Create your views here.

@login_required
def Paquetes (request):
    paquete= Paquete.objects.all()
    paquetes_inactivos= Paquete.objects.exclude(fechaCaducidad_paquete=None)
    paquetes_activos=Paquete.objects.filter(fechaCaducidad_paquete=None)
    return render(request, "Paquetes.html", {"paquetes": paquete,"paquetes_activos":paquetes_activos,"paquetes_inactivos":paquetes_inactivos})

@login_required
def registrarPaquete(request):
    clases=request.POST['numClases']
    precio=request.POST['numPrecio']
    
    try:
        paquete = Paquete.objects.create(cant_clas_sem=clases,precio_paquete=precio)
         
    except:
        print("algo salio mal")
        pass
    
    return redirect('/Paquetes/')

@login_required
def eliminarPaquete(request, id_paquete):
    fecha_actual = timezone.now()
    # Si solo necesitas la fecha en formato de cadena, puedes usar strftime
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")

    try:
        paquete=Paquete.objects.get(id_paquete=id_paquete)
        
        paquete.fechaCaducidad_paquete=fecha_actual_str
        paquete.save()
    except:
        print("eliminacion fallida")
    try:
        return redirect ("/Paquetes/")
    except:
        print("redireccion fallida")

@login_required
def activarPaquete(request,id_paquete):
    try:
        paquete=Paquete.objects.get(id_paquete=id_paquete)
        
        paquete.fechaCaducidad_paquete=None
        paquete.save()
    except:
        print("eliminacion fallida")
    try:
        return redirect ("/Paquetes/")
    except:
        print("redireccion fallida")
        