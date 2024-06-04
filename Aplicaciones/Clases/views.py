from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Clase,Recibo,Reserva
from Aplicaciones.clientes.models import Cliente
from Aplicaciones.Turnos.models import Turnos
from Aplicaciones.Paquetes.models import Paquete
import json
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime ,timedelta
# Create your views here.


@login_required
def menuClases(request):
    # Renderizar el template con los datos necesarios
    
    return render(request, "menuClases.html")

@login_required
def crearRecibo(request):
    # Obtener todos los clientes de la base de datos
    clientes = Cliente.objects.all()
    
    # Renderizar el template con los datos necesarios
    return render(request, "crearRecibo.html", {"clientes": clientes})

@login_required
def guardarRecibo(request):
    
    fecha_actual = datetime.now().date()

    # Sumarle 30 días
    fecha_en_30_dias = fecha_actual + timedelta(days=30)

    # Obtener los datos del formulario
    dni_ingresado = request.POST['DNIRecibo']
    fecha = request.POST['fechaRecibo']
    importe = request.POST['numImporte']
    metodo_pago = request.POST["pagoRecibo"]
    DNI=Cliente.objects.get(dni=dni_ingresado)
    
    try:
        # Crear un nuevo recibo con los datos proporcionados
        recibo = Recibo.objects.create(dni=DNI, fecha_recibo=fecha, importe=importe, métodoDePago=metodo_pago)
        DNI.fecha_baja=fecha_en_30_dias
        DNI.save()
    except Exception as e:
        print("Fallo al ingresar datos:", e)
    
    # Redirigir a la página de inicio
    return redirect('/menuClases/')

@login_required
def verRecibo(request):
    # Obtener todos los recibos de la base de datos
    recibos = Recibo.objects.all()
    # Renderizar el template con los datos necesarios
    return render(request, "verRecibo.html", {"recibos": recibos})

@login_required
def crearClase(request):
    # Obtener los paquetes activos, todos los clientes y los recibos no utilizados de la base de datos
    paquete = Paquete.objects.filter(fechaCaducidad_paquete=None)
    clientes = Cliente.objects.all()
    recibos = Recibo.objects.filter(usado=None)
    
    # Crear un diccionario de recibos para serializar a JSON
    recibos_dict = {}
    for i in recibos:
        recibos_dict[i.id_recibo] = i.dni.dni
    recibos_json = json.dumps(recibos_dict)
      
    # Renderizar el template con los datos necesarios
    return render(request, "crearReserva.html", {"paquete": paquete, "clientes": clientes, "recibos_json": recibos_json})

@login_required
def elegirProcedimiento(request):
    turnos_libres()
    
    
    return render(request, "elegirProcedimiento.html")

@login_required
def crearClasePreferencia(request):
    paquete = Paquete.objects.filter(fechaCaducidad_paquete=None)
    clientes = Cliente.objects.all()
    recibos = Recibo.objects.filter(usado=None)
    
    # Crear un diccionario de recibos para serializar a JSON
    recibos_dict = {}
    for i in recibos:
        recibos_dict[i.id_recibo] = i.dni.dni
    recibos_json = json.dumps(recibos_dict)
      
    return render(request, "crearClasePreferencia.html", {"paquete": paquete, "clientes": clientes, "recibos_json": recibos_json})

@login_required
def crearClasePreferenciaParte2(request):
    # Obtener todos los turnos de la base de datos
    turnos_libres_list=turnos_libres()
    list_turnos=[]
    for i in turnos_libres_list:
        list_turnos.append(i[0])
    turnos = Turnos.objects.filter(id_turno__in=list_turnos)
    
    # Crear un diccionario de turnos para serializar a JSON
    turnos_dict = {}
    for i in turnos:                             
        turnos_dict[i.id_turno] = [i.rango_turno, i.dia_turno]
    turnos_json = json.dumps(turnos_dict)
    dni = request.POST['DNIReserva']
    try:
        recibo = request.POST['numRecibo']
    except:
        recibo = None
    paquete = request.POST['numPaquete']
    # Obtener la cantidad de fechas del paquete seleccionado
    cant_fechas = Paquete.objects.get(id_paquete=paquete)
    cant_fechas = cant_fechas.cant_clas_sem
    # Serializar los datos de reserva a JSON
    datos_reserva = [dni, paquete, recibo]
    datos_reserva_json = json.dumps(datos_reserva)
    # Renderizar el template con los datos necesarios
    return render(request, "crearClasePreferencia-parte2.html", {"turnos_json": turnos_json, "cant_fechas": cant_fechas, "datosReserva": datos_reserva_json})

@login_required
def crearClasePreferenciaParte3(request):
    # Diccionario para convertir nombres de días de la semana a números
    dias_semana = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "domingo": 6
    }
    
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    
    if request.method == 'POST':
        # Acceder a los datos enviados desde los campos ocultos
        cant_fechas = request.POST.get('cant_fechas')
        datos_reserva_str = request.POST.get('datosReserva')
        datos_reserva = json.loads(datos_reserva_str)
        
        # Obtener los objetos relacionados a partir de los datos de reserva
        recibo = Recibo.objects.get(id_recibo=datos_reserva[2])
        paquete = Paquete.objects.get(id_paquete=datos_reserva[1])
        
        # Crear una nueva reserva con la fecha actual
        reserva = Reserva.objects.create(DNI=datos_reserva[0], id_paquete=paquete, id_recibo=recibo, fecha_reserva=fecha_actual_str)
    
        # Acceder a los datos de los campos select
        cantidad_fechas = int(cant_fechas)
        for i in range(1, cantidad_fechas + 1):
            seleccion = request.POST.get(f'select_{i}')
            turno = Turnos.objects.get(id_turno=seleccion)
            dia_semana = dias_semana[turno.dia_turno]
            
            # Calcular cuántos días faltan hasta el próximo día seleccionado
            dias_hasta_proximo_dia = (dia_semana - fecha_actual.weekday() + 7) % 7
            
            # Crear clases para las próximas 4 semanas
            for j in range(4):
                fecha_siguiente = fecha_actual + timedelta(days=dias_hasta_proximo_dia + j * 7)
                fecha_clase = fecha_siguiente.strftime("%Y-%m-%d")
                try:
                    # Crear una clase con el turno y la reserva correspondientes
                    clase = Clase.objects.create(id_turno=turno, id_reserva=reserva, fecha_clase=fecha_clase)
                except:
                    # Manejar errores al crear clases
                    print("Clase", j, "=", int(turno.id_turn), reserva.id_reserva, fecha_clase)
                    print("Fallo al crear registro", j, "de clase")
                
            
            # Guardar la fecha de uso del recibo
            try:
                recibo.usado = fecha_actual_str
                recibo.save()
            except:
                # Manejar errores al cambiar la fecha de uso del recibo
                print("Fallo al cambiar registro de recibo")

        # Redireccionar a otra página tras procesar los datos
        return redirect('/')
    
    # Si no es una petición POST, puedes decidir qué hacer, por ejemplo, mostrar el formulario.
    else:
        pass
        
    # Redireccionar a la página de inicio
    return redirect("/")

@login_required
def crearClaseParte2(request):
    # Obtener todos los turnos de la base de datos
    turnos_libres_list=turnos_libres()
    list_turnos=[]
    for i in turnos_libres_list:
        list_turnos.append(i[0])
    turnos = Turnos.objects.filter(id_turno__in=list_turnos)
    
    # Crear un diccionario de turnos para serializar a JSON
    turnos_dict = {}
    for i in turnos:                             
        turnos_dict[i.id_turno] = [i.rango_turno, i.dia_turno]
    turnos_json = json.dumps(turnos_dict)
    
    # Obtener los datos del formulario
    dni = request.POST['DNIReserva']
    try:
        recibo = request.POST['numRecibo']
    except:
        recibo = None
    paquete = request.POST['numPaquete']
    
    # Obtener la cantidad de fechas del paquete seleccionado
    cant_fechas = Paquete.objects.get(id_paquete=paquete)
    cant_fechas = cant_fechas.cant_clas_sem
    
    
    
    # Serializar los datos de reserva a JSON
    datos_reserva = [dni, paquete, recibo]
    datos_reserva_json = json.dumps(datos_reserva)
    
    # Renderizar el template con los datos necesarios
    return render(request, "elegir_fechas.html", {"turnos_json": turnos_json, "cant_fechas": cant_fechas, "datosReserva": datos_reserva_json})

@login_required
def crearClaseParte3(request):
    # Obtener la fecha actual
    fecha_actual = timezone.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    
    # Recuperar los datos del formulario
    fechas = []
    turnos = []
    dict_reserva = {"dni": None, "paquete": None, "recibo": None}
    contador = 0
    reserva = None
    
    # Recuperar los turnos seleccionados del campo oculto
    turnos_seleccionados_str = request.POST.get('turnos_seleccionados')
    turnos_seleccionados = json.loads(turnos_seleccionados_str)
    
    # Manejar los datos de los turnos seleccionados
    if request.method == 'POST':
        datos_reserva_json = request.POST.get('datos_reserva')
        if datos_reserva_json is not None:
            try:
                datos_reserva = json.loads(datos_reserva_json)
                
            except json.JSONDecodeError as e:
                print(f"Error al cargar datos de reserva: {e}")
        
        # Asignar los datos de reserva
        for i in dict_reserva:
            dict_reserva[i] = int(datos_reserva[contador])
            
            contador += 1
    else:
        pass
        # La solicitud no es POST, puede manejarla de acuerdo a tus necesidades
    
    # Obtener el paquete y recibo
    paquete = Paquete.objects.get(id_paquete=int(dict_reserva["paquete"]))
    recibo = Recibo.objects.get(id_recibo=int(dict_reserva["recibo"]))
    
    
    # Crear la reserva
    reserva = Reserva.objects.create(DNI=str(dict_reserva["dni"]), id_paquete=paquete, id_recibo=recibo, fecha_reserva=fecha_actual_str)
    
    # Ahora puedes trabajar con los turnos seleccionados
    for i in range(4):
        for x in range(paquete.cant_clas_sem):
            fecha = request.POST.get('fecha-semana-' + str(i + 1) + "-" + str(x + 1))
            fechas.append(fecha)
            if turnos_seleccionados.get("select-fecha-semana-" + str(i + 1) + "-" + str(x + 1)) != "":
                turnos.append(turnos_seleccionados.get("select-fecha-semana-" + str(i + 1) + "-" + str(x + 1)))
            else:
                turnos.append(None)
    
    # Crear las clases
    for i in range(len(fechas)):
        try:
            turno = Turnos.objects.get(id_turno=int(turnos[i]))
            clase = Clase.objects.create(id_turno=turno, id_reserva=reserva, fecha_clase=fechas[i])
        except:
            print("Clase", i, "=", int(turnos[i]), reserva.id_reserva, fechas[i])
            print("Fallo al crear registro", i, "de clase")
    
    # Actualizar el recibo
    try:
        recibo.usado = fecha_actual_str
        recibo.save()
    except:
        print("Fallo al cambiar registro de recibo")
    
    #redirijir al menu
    return redirect("/menuClases/")

@login_required
def verClases(request):
    # Obtener la fecha y hora actual
    fecha_actual = timezone.now()

    # Obtener todas las clases que no han sido canceladas
    clases = Clase.objects.filter(fecha_cancelado=None)

    # Obtener todos los turnos que no han sido dados de baja
    turnos = Turnos.objects.filter(fecha_baja=None)

    # Obtener el ID del turno si se proporciona en la consulta GET
    turno = request.GET.get("txtTurno")

    # Obtener la fecha mínima si se proporciona en la consulta GET
    fechaMinima = request.GET.get('fechaMinima')

    # Obtener la fecha si se proporciona en la consulta GET
    fecha = request.GET.get('fecha')

    # Obtener el día de la semana si se proporciona en la consulta GET
    dia = request.GET.get('dia')

    # Obtener el nombre y apellido si se proporcionan en la consulta GET
    nombre = request.GET.get('nombre')
    apellido = request.GET.get('apellido')

    # Convertir la fecha actual a formato de cadena YYYY-MM-DD
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")

    # Filtrar las clases según la fecha mínima si se proporciona
    if fechaMinima:
        fecha_parsed = parse_date(fechaMinima)
        clases = clases.filter(fecha_clase__gte=fecha_parsed)
    else:
        clases = clases.filter(fecha_clase__gte=fecha_actual_str)

    # Filtrar las clases según el turno si se proporciona
    if turno:
        clases = clases.filter(id_turno=str(turno))

    # Filtrar las clases según la fecha si se proporciona
    if fecha:
        fecha_parsed = parse_date(fecha)
        clases = clases.filter(fecha_clase=fecha_parsed)

    # Filtrar las clases según el día de la semana si se proporciona
    if dia:
        clases = clases.filter(id_turno__dia_turno=dia)

    # Filtrar las clases según el nombre si se proporciona
    if nombre:
        clases = clases.filter(id_reserva__id_recibo__dni__nombre__icontains=nombre)

    # Filtrar las clases según el apellido si se proporciona
    if apellido:
        clases = clases.filter(id_reserva__id_recibo__dni__apellido__icontains=apellido)

    # Renderizar el template con las clases y los turnos filtrados
    return render(request, "verClase.html", {"clases": clases, "turnos": turnos})

@login_required
def editarClase(request, id_clase):
    # Diccionario para convertir nombres de días de la semana a español
    dias_semana_espanol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    
    # Obtener la clase con el ID proporcionado
    clase = Clase.objects.get(id_clase=id_clase)
    
    # Obtener la fecha de la clase y su día de la semana
    fecha = clase.fecha_clase
    dia_semana = fecha.strftime("%A")
    fecha = str(fecha)
    
    
    # Filtrar los turnos para el día de la semana de la clase
    turnos = Turnos.objects.filter(dia_turno=dias_semana_espanol[dia_semana].lower())
    
    
    
    # Renderizar la plantilla con los datos de la clase y los turnos
    return render(request, "edicionClase.html", {'clase': clase, "fecha": fecha, "turnos": turnos})

@login_required
def edicionClase(request):
    # Obtener datos del formulario
    id_clase = request.POST.get("txtId_clase")
    id_turno = request.POST.get("txtTurno")
    fecha_clase = request.POST.get("dateFecha")
    asistencia = request.POST.get("txtAsistencia")
    preparacion = request.POST.get("txtPreparacion")
    observaciones = request.POST.get("txtObservaciones")
    
    # Verificar si la asistencia es "None" y ajustarla si es necesario
    if asistencia == "None":
        asistencia = None 
    
    # Obtener la clase existente
    clase = Clase.objects.get(id_clase=id_clase)
    turno = Turnos.objects.get(id_turno=id_turno)
    
    # Verificar si se necesitan realizar cambios en la clase
    if str(id_turno) != str(clase.id_turno.id_turno) or str(fecha_clase) != str(clase.fecha_clase):
        # Actualizar el campo fecha_cancelado del registro existente con la fecha actual
        clase.fecha_cancelado = datetime.now().date()
        
        # Crear una nueva clase con los datos actualizados
        nueva_clase = Clase.objects.create(
            id_turno=turno,
            id_reserva=clase.id_reserva,
            fecha_clase=fecha_clase,
            asistencia=asistencia,
            preparacion=preparacion,
            observaciones=observaciones
        )
        
        # Asignar la nueva clase a la clase anterior
        clase.nueva_clase = nueva_clase
        clase.save()
    else:
        # Actualizar los datos de la clase existente
        clase.asistencia = asistencia
        clase.observaciones = observaciones
        clase.preparacion = preparacion
        clase.save()
        
    # Redireccionar a la página de visualización de clases
    return redirect("/menuClases/verClases/")



#Funciones:
def fecha_inicio_proxima_semana():
    hoy = datetime.now()
    dia_semana_actual = hoy.weekday()
    dias_para_lunes_proxima_semana = (7 - dia_semana_actual) % 7
    inicio_proxima_semana = hoy + timedelta(days=dias_para_lunes_proxima_semana)
    # Agregar la hora deseada (por ejemplo, 8:00 AM)
    inicio_proxima_semana_con_hora = inicio_proxima_semana.replace(hour=8, minute=0, second=0, microsecond=0)
    return inicio_proxima_semana_con_hora


def turnos_libres():
    dias_semana = {
        'Monday': 'lunes',
        'Tuesday': 'martes',
        'Wednesday': 'miercoles',
        'Thursday': 'jueves',
        'Friday': 'viernes',
        'Saturday': 'sabado',
        'Sunday': 'domingo'
    }
    
    fecha = fecha_inicio_proxima_semana()  # No es necesario convertir a str y luego a datetime
    proximas_clases = Clase.objects.filter(fecha_clase__gte=fecha)
    turnos_activos = Turnos.objects.filter(fecha_baja=None)
    turnos_dict={}
    for i in turnos_activos:
        turnos_dict[i.id_turno]=[True,999] 
    
    for i in range(7*4):
        nombre_dia_semana = fecha.strftime('%A')
        #print(fecha.strftime("%Y-%m-%d")
        # , dias_semana[nombre_dia_semana])
        turnos=Turnos.objects.filter( dia_turno=dias_semana[nombre_dia_semana],fecha_baja=None)
        
        for x in turnos:
            clases=Clase.objects.filter(fecha_clase=fecha,id_turno=x)
            
            
            if int(x.cant_maxima)<=int(len(clases)) or turnos_dict[x.id_turno]==False:
                
                turnos_dict[x.id_turno][0]=False
                turnos_dict[x.id_turno][1]=0
            else:
                if int(x.cant_maxima)-int(len(clases))<=turnos_dict[x.id_turno][1]:
                    turnos_dict[x.id_turno][1]=int(x.cant_maxima)-int(len(clases))
        
        fecha += timedelta(days=1)
    
    turnos_libres_list=[]
    for i in turnos_dict:
        if turnos_dict[i][0]==True:
            dato=[i,turnos_dict[i][1]]
            turnos_libres_list.append(dato)
    
    return turnos_libres_list  

