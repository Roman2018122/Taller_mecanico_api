# Backen con django rest framework 
###  Tema: Taller mecanico
### Autor:  Jonathan Torres
### Descripcion del proyecto
#### Este proyecto es un backend desarrollado en Django REST Framework para la gestión de un taller mecánico. Permite administrar clientes, vehículos, servicios, mecánicos, órdenes de reparación y detalles de servicio.
#### Incluye autenticación mediante JWT y control de permisos por roles (usuario normal y administrador).

## Instalacion y ejecucion 
### Requisitos
#### Python 3.10+
#### PostgreSQL
#### pip
#### virtualenv

## Clonar repositorio:
### git clone https://github.com/Roman2018122/torres_taller_api.git 
### cd taller_api

## Crear Entorno virtual:
### python -m venv venv

## Activar
### windows: venv\Scripts\activate

### pip install -r requirements.txt

## Migraciones 
### python manage.py makemigrations
### python manage.py migrate

## Crear super usuario
### python manage.py createsuperuser

## Autenticacion JWT
### POST /api/login/

### body 
#### {
  #### "username": "taller_user",
  #### "password": "taller123"
#### }
### Respuesta

#### {
  #### "refresh": "token_refresh",
  #### "access": "token_access"
#### }

## En POSTMAN 
#### Authorization: Bearer <access_token>
### Endpoints de la API
#### Clientes
#### Vehiculos
#### Servicios
#### Mecanicos
#### Orden reparacion 
#### Detalle servicio

## Ejemplo de uso  POST con token :
#### POST /api/Cliente/

#### Authorization: Bearer eyJ...
#### Content-Type: application/json

#### {
  #### "nombre": "Juan Perez",
  #### "telefono": "0999999999",
  #### "correo": "juan@gmail.com",
  #### "direccion": "Quito"
#### }

## Permisos del sistema 
## Usuario normal
### Solo lectura (GET)
## Administrador
### CRUD completo (POST, PUT, DELETE)