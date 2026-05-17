# SleepCare Band PRO+

SleepCare Band PRO+ es un sistema IoT desarrollado para monitorear el sueño y el estado de salud de adultos mayores mediante una pulsera inteligente basada en ESP32.  
El sistema permite registrar datos biométricos como ritmo cardíaco, oxígeno en sangre, temperatura corporal y movimiento, para luego enviarlos a una API creada con Django.

---

## ¿Para qué sirve este proyecto?

Este proyecto sirve para que familiares, cuidadores o personal autorizado puedan visualizar información de salud del adulto mayor y recibir alertas cuando se detecte una situación de riesgo.

Por ejemplo:

- Ritmo cardíaco fuera de rango.
- Oxígeno bajo.
- Temperatura corporal elevada.
- Movimiento anormal o posible caída.
- Activación de alerta desde el dispositivo.

---

## ¿Cómo funciona el sistema?

El funcionamiento general es el siguiente:

```text
ESP32 / Pulsera inteligente
        ↓
Sensores biométricos
        ↓
Conexión WiFi
        ↓
API REST en Django
        ↓
Base de datos MySQL
        ↓
Panel administrador / Dashboard






---

## Explicación de los archivos principales

### models.py

Este archivo contiene la estructura de la base de datos del sistema.  
Aquí se crean todas las tablas principales del proyecto utilizando modelos de Django.

Por ejemplo:

- Paciente
- Usuario
- Dispositivo
- RegistroSalud
- Alerta

Cada modelo representa una tabla dentro de MySQL.

También se definen:
- relaciones entre tablas
- claves foráneas
- tipos de datos
- restricciones

---

### serializers.py

Este archivo se encarga de convertir los datos entre Django y formato JSON.

Su función principal es permitir que la API pueda:

- recibir datos desde el ESP32
- enviar datos hacia aplicaciones externas
- transformar modelos en JSON

Por ejemplo:

```python
class RegistroSaludSerializer(serializers.ModelSerializer):
```

permite convertir un registro de salud en un JSON para la API REST.

Sin serializers:
- el ESP32 no podría enviar datos correctamente
- la API no podría responder en formato JSON

---

### views.py

Este archivo contiene la lógica principal de las APIs.

Aquí se crean las vistas que:
- reciben peticiones HTTP
- guardan datos
- consultan información
- responden al ESP32 o al frontend

Se utilizan ViewSets de Django REST Framework para generar automáticamente:

- GET
- POST
- PUT
- DELETE

Por ejemplo:

```python
class RegistroSaludViewSet(viewsets.ModelViewSet):
```

permite:
- registrar datos biométricos
- listar registros
- editar registros
- eliminar registros

---

### urls.py

Este archivo define las rutas del sistema y de las APIs.

Ejemplo:

```python
path("api/", include("monitoreo.urls"))
```

Esto permite acceder a:

```text
/api/registros-salud/
/api/pacientes/
/api/alertas/
```

Las URLs son necesarias para conectar:
- ESP32
- frontend
- aplicaciones móviles
- APIs externas

---

### admin.py

Este archivo sirve para registrar los modelos en el panel administrador de Django.

Gracias a este archivo es posible administrar:

- pacientes
- usuarios
- dispositivos
- alertas
- registros de salud

desde:

```text
http://127.0.0.1:8000/admin/
```

---

### settings.py

Este archivo contiene toda la configuración principal del proyecto.

Aquí se configuran:

- base de datos MySQL
- aplicaciones instaladas
- archivos estáticos
- Django REST Framework
- panel Unfold
- idioma
- zona horaria

También se configura:
- el logo del sistema
- estilos personalizados
- conexión de APIs

---

### manage.py

Es el archivo principal de administración de Django.

Permite ejecutar comandos importantes como:

```bash
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

Es necesario para administrar y ejecutar el proyecto.

---

### static/

Esta carpeta almacena archivos estáticos del sistema como:

- imágenes
- logos
- CSS
- estilos personalizados

Por ejemplo:

```text
static/img/logo.png
static/css/admin.css
```

---

### migrations/

Esta carpeta almacena las migraciones de la base de datos.

Cada vez que se modifica un modelo:

```python
models.py
```

Django genera archivos de migración para actualizar MySQL automáticamente.

---

### requirements.txt

Este archivo almacena todas las librerías necesarias del proyecto.

Permite instalar automáticamente todas las dependencias usando:

```bash
pip install -r requirements.txt
```

Esto facilita:
- compartir el proyecto
- subirlo a GitHub
- desplegarlo en servidores