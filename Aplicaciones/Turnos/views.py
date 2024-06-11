from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Turnos
from Aplicaciones.Clases.views import turnos_libres
# Create your views here.

@login_required
def turnos(request):
    turnos= Turnos.objects.all()
    turnos_inactivos= Turnos.objects.exclude(fecha_baja=None)
    turnos_activos=Turnos.objects.filter(fecha_baja=None)
    return render(request, "Turnos.html", {"turnos": turnos,"turnos_activos":turnos_activos,"turnos_inactivos":turnos_inactivos})

@login_required
def registrarTurno(request):
    dia=request.POST['txtDia']
    horarioinicio=request.POST['txtHorarioinicio']
    horariofinal=request.POST['txtHorariofinal']
    cantidad=request.POST['numCant']
    horario=str(horarioinicio)+"-"+str(horariofinal)
    
    try:
        turnos = Turnos.objects.create(dia_turno=dia, rango_turno=horario, cant_maxima=cantidad)    
    except:
        print("algo salio mal")
        pass
    return redirect('/Turnos/')

@login_required
def eliminarTurno(request, id_turno):
    fecha_actual = timezone.now()
    # Si solo necesitas la fecha en formato de cadena, puedes usar strftime
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    try:
        turno=Turnos.objects.get(id_turno=id_turno)
        turno.fecha_baja=fecha_actual_str
        turno.save()
    except:
        print("eliminacion fallida")
    try:
        return redirect ("/Turnos/")
    except:
        print("redireccion fallida")
        
@login_required
def activarTurno(request, id_turno):
    try:
        turno=Turnos.objects.get(id_turno=id_turno)
        turno.fecha_baja=None
        turno.save()
    except:
        print("eliminacion fallida")
    try:
        return redirect ("/Turnos/")
    except:
        print("redireccion fallida")

@login_required
def turnosDisponibles(request):
    turnos_libres_list=turnos_libres()
    list_turnos=[]
    for i in turnos_libres_list:
        list_turnos.append(i[0])
    turnos = Turnos.objects.filter(id_turno__in=list_turnos)
    
    
    return render(request,"turnosDisponibles.html",{"turnos":turnos,"cantidad":turnos_libres})
    

