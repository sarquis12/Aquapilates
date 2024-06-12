# Aquapilates Web App

Este es un proyecto de una página web para una empresa de aquapilates. La aplicación permite la gestión de turnos,paquetes, el registro de clientes y la programación de clases de aquapilates. El proyecto está desarrollado utilizando Django y Python.

## Requisitos

- Python 3.x
- Django 3.x

## Instalación

1. Clona este repositorio en tu máquina local:
2.Ejecuta las migraciones de la base de datos:
-python manage.py migrate
3.Inicia el servidor de desarrollo:
-python manage.py runserver

##Uso
La aplicación permite realizar las siguientes acciones:

Crear, ver, editar y eliminar turnos.
Registrar nuevos clientes.
Programar clases de aquapilates, asignando clientes a cada clase.
Visualizar el horario de clases y la disponibilidad de turnos

##Estado del Proyecto
Versión actual: 0.1.0 (en desarrollo)
Última actualización: 5de Abril del 2024

##Actualización de deploy :
1- volver a la "screen" llamada "django-server" con el siguiente codigo:
screen -r django-server
2-detener el proceso con "ctrl+C"
3-salir del screen presionando Ctrl + A seguido de D
4-estando en la carpeta "PROJECT" usando "cd /opt/bitnami/projects/PROJECT"  ejecutar "git pull origin master" para actualizar el repositorio al mas actualizado

5-verificar los cambios
6- settings.py debera configurarse para conectarse a la db
7-sincronizar la db ejecutando los siguientes comandos:
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate --fake
8- volver a la screen usando el comando del paso 1 y activar servidor usando:
python manage.py runserver 0.0.0.0:8000


##acticar servidor
1- ubicarse en la carpeta "PROJECT"
2- si no existe, una sesion de  "screen" con el nombre "django-server" usando el siguiente comando :
screen -S django-server
si la sesion existe, entrar a esta con el comando 
screen -r django-server
3-una vez en la sesion, utilizar el comando runserver
python manage.py runserver 0.0.0.0:8000
4- salir de la sesion presionando Ctrl + A seguido de D