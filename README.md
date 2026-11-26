# Smart_Connect

## Descripción del proyecto

SmartConnect es un sistema de gestión de terrenos, viviendas, usuarios y puntos de acceso desarrollado mediante una API REST.

El sistema permite administrar registros, asignar residentes a viviendas y controlar los permisos de los usuarios mediante autenticación JWT.

## Tecnologías utilizadas

- Python 3.13
- Django 6.1
- Django REST Framework
- SimpleJWT
- SQLite
- Django Admin
- Apidog
- Git y GitHub

## Funcionalidades implementadas

- CRUD de usuarios.
- CRUD de terrenos.
- CRUD de viviendas.
- CRUD de puntos de acceso.
- Asignación de residentes a viviendas.
- Validación de asignaciones duplicadas.
- Autenticación mediante JWT.
- Obtención y renovación de tokens.
- Control de permisos por terreno y vivienda.
- Protección de registros con relaciones existentes.
- Administración de datos mediante Django Admin.
- Pruebas automatizadas y manuales mediante Apidog.

## Instalación del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/olivaresmarcos02-wq/Smart_Connect.git
cd Smart_Connect
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

Windows mediante Git Bash:

```bash
source venv/Scripts/activate
```

Linux o macOS:

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias principales

```bash
python -m pip install Django==6.1 djangorestframework==3.18.3 djangorestframework-simplejwt==5.5.1
```

El archivo requirements.txt contiene las dependencias registradas durante el desarrollo. El comando anterior instala las dependencias principales necesarias para ejecutar SmartConnect.

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

Este comando crea las tablas correspondientes en la base de datos SQLite.

### 6. Crear un administrador

```bash
python manage.py createsuperuser
```

Ingresar el nombre de usuario, correo electrónico y contraseña solicitados.

### 7. Verificar el proyecto

```bash
python manage.py check
```

### 8. Iniciar el servidor

```bash
python manage.py runserver
```

## Acceso al sistema

| Servicio | Dirección |
| --- | --- |
| Django Admin | http://127.0.0.1:8000/admin/ |
| API REST | http://127.0.0.1:8000/api/ |
| Login JWT | http://127.0.0.1:8000/api/token/ |
| Renovación JWT | http://127.0.0.1:8000/api/token/refresh/ |

## Estructura del proyecto

```text
Smart_Connect/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── inventory/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Modelo de datos

| Entidad | Descripción |
| --- | --- |
| Usuario | Almacena los datos personales y su vínculo con una cuenta de Django. |
| Terreno | Representa una propiedad y sus administradores. |
| Vivienda | Representa una vivienda perteneciente a un terreno. |
| PuntoAcceso | Representa una entrada asociada a un terreno y sus horarios. |
| Residente | Relaciona un usuario con una vivienda y su tipo de participación. |
| Equipment | Modelo de equipos conservado del avance anterior. |


## Endpoints de la API REST

| Recurso | Endpoint |
| --- | --- |
| Usuarios | /api/usuarios/ |
| Terrenos | /api/terrenos/ |
| Viviendas | /api/viviendas/ |
| Puntos de acceso | /api/puntos-acceso/ |
| Residentes | /api/residentes/ |
| Equipos | /api/equipos/ |
| Login JWT | /api/token/ |
| Renovación JWT | /api/token/refresh/ |

### Métodos HTTP

| Método | Descripción |
| --- | --- |
| GET | Listar registros o consultar un registro específico. |
| POST | Crear un registro. |
| PUT | Actualizar completamente un registro. |
| PATCH | Actualizar parcialmente un registro. |
| DELETE | Eliminar un registro. |

Los cuatro CRUD maestros permiten utilizar estos métodos según los permisos del usuario autenticado.

El recurso Residentes permite listar, consultar y crear asignaciones mediante la API.

Para consultar un registro específico se debe agregar su identificador al endpoint.

Ejemplo:

```http
GET /api/viviendas/3/
```

## Autenticación JWT

El sistema utiliza JSON Web Token (JWT) para identificar a los usuarios que realizan peticiones a la API.

### Obtener token

Realizar una petición POST desde Apidog:

```http
POST http://127.0.0.1:8000/api/token/
```

Body en formato JSON:

```json
{
    "username": "usuario_prueba",
    "password": "tu_contraseña"
}
```

La respuesta contiene dos tokens:

```json
{
    "refresh": "token_de_renovacion",
    "access": "token_de_acceso"
}
```

### Utilizar el token

En Apidog, seleccionar:

Auth → Bearer Token

Ingresar el contenido del token access.

También se puede utilizar el encabezado:

```http
Authorization: Bearer TOKEN_ACCESS
```

### Renovar el token

```http
POST http://127.0.0.1:8000/api/token/refresh/
```

Body:

```json
{
    "refresh": "TOKEN_REFRESH"
}
```

La configuración actual establece una duración de una hora para el token de acceso y un día para el token de renovación.

## Roles y permisos

El sistema controla las operaciones según la cuenta autenticada y sus relaciones con los terrenos y viviendas.

### Administrador general

- Crear, consultar, modificar y eliminar registros maestros.
- Consultar todos los terrenos y viviendas.
- Asignar residentes.
- Conceder el tipo de participación Propietario administrador.

### Propietario administrador

- Consultar los terrenos y viviendas que tiene autorizados.
- Consultar residentes de las viviendas que administra.
- Asignar residentes dentro de su alcance.
- No puede administrar viviendas ajenas.
- No puede conceder el tipo de participación Propietario administrador.

### Arrendatario

- Consultar las viviendas donde se encuentra registrado.
- Consultar los terrenos y puntos de acceso asociados.
- Consultar su información personal.
- No puede asignar residentes.
- No puede modificar los registros maestros.

### Matriz de permisos

| Funcionalidad | Administrador general | Propietario administrador | Arrendatario |
| --- | --- | --- | --- |
| CRUD de maestros | Sí | No | No |
| Consultar terrenos | Todos | Autorizados | Asociados |
| Consultar viviendas | Todas | Autorizadas | Asociadas |
| Asignar residentes | Sí | Dentro de su alcance | No |
| Conceder rol administrativo | Sí | No | No |

## Ejemplos de peticiones en Apidog

### Crear usuario

```http
POST /api/usuarios/
```

```json
{
    "rut": "12345678-5",
    "nombre": "Pedro",
    "apellido": "Gonzalez",
    "telefono": "+56912345678",
    "correo": "pedro@example.com",
    "estado": true
}
```

### Crear terreno

```http
POST /api/terrenos/
```

```json
{
    "nombre": "Condominio Norte",
    "direccion": "Avenida Norte 100",
    "estado": true
}
```

### Crear vivienda

```http
POST /api/viviendas/
```

```json
{
    "terreno": 1,
    "numero": 101,
    "estado": true
}
```

### Crear punto de acceso

```http
POST /api/puntos-acceso/
```

```json
{
    "terreno": 1,
    "nombre": "Entrada principal",
    "hora_desde": "08:00",
    "hora_hasta": "22:00"
}
```

Los identificadores utilizados en los ejemplos deben reemplazarse por los correspondientes a cada base de datos.

## Operación del negocio

La operación principal del negocio implementada en este avance consiste en asignar una persona a una vivienda mediante el modelo Residente.

Los tipos de participación disponibles son:

- PROPIETARIO_ADMIN
- PROPIETARIO
- ARRENDATARIO

### Asignar residente

```http
POST /api/residentes/
```

```json
{
    "usuario": 6,
    "vivienda": 3,
    "rol_residente": "ARRENDATARIO"
}
```

### Reglas del negocio

- La persona debe existir y encontrarse activa.
- La vivienda debe existir y encontrarse activa.
- El terreno debe encontrarse activo.
- El solicitante debe tener autorización sobre la vivienda.
- No se permite asignar dos veces a la misma persona a una misma vivienda.
- Un arrendatario no puede realizar asignaciones si no tiene funciones administrativas.
- Los propietarios administradores no pueden asignar residentes fuera de su alcance.
- Las operaciones rechazadas no deben generar registros en la base de datos.
- No se permite eliminar registros cuando existen relaciones protegidas.

## Preparación de datos de prueba

Los datos iniciales pueden ingresarse mediante Django Admin.

### Cuentas de autenticación

| Cuenta | Tipo |
| --- | --- |
| Administrador | Cuenta con permiso staff |
| propietario | Cuenta normal |
| arrendatario | Cuenta normal |

### Usuarios de prueba

| Nombre | Apellido | Cuenta vinculada |
| --- | --- | --- |
| Carlos | Pérez | propietario |
| María | González | arrendatario |

### Terrenos de prueba

| Nombre | Administrador |
| --- | --- |
| Condominio Norte | Carlos Pérez |
| Condominio Sur | Sin Carlos como administrador |

### Viviendas de prueba

| Número | Terreno |
| --- | --- |
| 101 | Condominio Norte |
| 201 | Condominio Sur |

Durante las pruebas, Carlos asignará a María como arrendataria de la vivienda 101.

Posteriormente se comprobará que Carlos no pueda asignar residentes en la vivienda 201 y que María no tenga autorización para realizar asignaciones.

Todos los datos utilizados deben ser ficticios.

## Pruebas automatizadas

Para ejecutar las pruebas del proyecto:

```bash
python manage.py test inventory
```

Las pruebas se encuentran en:

```text
inventory/tests.py
```

| Prueba | Descripción |
| --- | --- |
| test_crud | Comprueba las operaciones de los cuatro CRUD maestros y la eliminación protegida. |
| test_asignacion | Comprueba las asignaciones válidas, duplicados y permisos. |
| test_jwt | Comprueba la autenticación, acceso protegido y renovación de tokens. |

Durante el desarrollo se aprobaron las tres pruebas automatizadas.

Resultado obtenido:

```text
Found 3 test(s).
System check identified no issues (0 silenced).

Ran 3 tests

OK
```

## Pruebas manuales en Apidog

Se realizaron pruebas manuales para comprobar el funcionamiento de los siguientes criterios:

### Criterio 1: Cuatro CRUD maestros integrados

- Crear registros.
- Listar registros.
- Consultar registros específicos.
- Actualizar registros.
- Eliminar registros.
- Comprobar la persistencia de los datos.
- Comprobar la protección de registros relacionados.

### Criterio 2: Operación del negocio

- Asignación correcta de un residente.
- Consulta de la asignación.
- Rechazo de asignaciones duplicadas.
- Rechazo de asignaciones fuera del alcance autorizado.
- Rechazo de asignaciones realizadas por un arrendatario sin funciones administrativas.
- Comprobación de que las operaciones rechazadas no modifican la base de datos.

### Criterio 3: Token JWT y permisos

- Obtención del token.
- Utilización del token.
- Renovación del token.
- Rechazo de peticiones sin autenticación.
- Rechazo de operaciones sin autorización.
- Filtrado de viviendas según los permisos del usuario.

## Códigos de respuesta HTTP

| Código | Descripción |
| --- | --- |
| 200 OK | Consulta, modificación o autenticación exitosa. |
| 201 Created | Registro creado correctamente. |
| 204 No Content | Registro eliminado correctamente. |
| 400 Bad Request | Datos incorrectos o incumplimiento de una regla del negocio. |
| 401 Unauthorized | Autenticación inexistente o token inválido. |
| 403 Forbidden | Usuario autenticado sin autorización. |
| 404 Not Found | Registro o recurso inexistente. |

## Base de datos

SmartConnect utiliza SQLite como base de datos local.

Django Admin y Apidog trabajan sobre la misma base de datos, permitiendo comprobar la persistencia de los registros.

La base de datos se genera mediante las migraciones de Django.

El archivo db.sqlite3 no se incluye en la versión actual del repositorio.

## Archivos excluidos del repositorio

El archivo .gitignore permite excluir archivos generados automáticamente, entornos virtuales y archivos locales.

```gitignore
__pycache__/
*.pyc
*.pyo
venv/
.venv/
db.sqlite3
.env
```

Las migraciones de Django se mantienen en el repositorio para permitir la instalación del proyecto en otros equipos.

## Alcance del segundo avance

El segundo avance contempla:

- Cuatro CRUD maestros integrados.
- Una operación del negocio.
- Autenticación JWT.
- Control de permisos.
- Validación de relaciones.
- Persistencia de datos.
- Pruebas automatizadas.
- Pruebas manuales mediante Apidog.

La implementación de credenciales RFID y registros de acceso físico queda fuera del alcance de este avance.

Los horarios de los puntos de acceso se almacenan, pero todavía no se utilizan para autorizar o rechazar accesos físicos.

## Consideraciones de seguridad

El proyecto está configurado para desarrollo y demostración académica en un entorno local.

Antes de realizar un despliegue en producción se debe:

- Configurar y renovar la clave secreta mediante variables de entorno.
- Desactivar el modo DEBUG.
- Configurar los hosts permitidos.
- Implementar HTTPS.
- Revisar los permisos de todas las rutas.
- Evitar publicar contraseñas y tokens JWT.

El recurso Equipment conserva la autenticación del avance anterior, pero no aplica las restricciones por terreno y vivienda de los CRUD maestros.

## Repositorio

https://github.com/olivaresmarcos02-wq/Smart_Connect


