# 🏋️ Gimnasio API - Estructura Base de Examen

Proyecto base reutilizable para examen de FastAPI con:

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Docker
- Docker Compose
- Arquitectura modular

---

# 📁 Estructura del Proyecto

gimnasio_api/
│
├── app/
│ ├── main.py
│ ├── database.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

---

# 🐳 Docker Compose

Contiene dos servicios:

## 🗄️ db (PostgreSQL)

- Imagen: postgres:15
- Usuario: postgres
- Password: postgres
- Base de datos: gimnasio_apolo_V
- Puerto: 5432
- Volumen persistente

## 🚀 api (FastAPI)

- Construido desde Dockerfile
- Puerto: 8000
- Depende del servicio db

---

# 🔌 Conexión a Base de Datos

Cadena de conexión utilizada:

⚠️ En Docker se usa el nombre del servicio `db`, no localhost.

---

# 📦 Dependencias

- fastapi
- uvicorn
- sqlalchemy
- psycopg
- pydantic
- python-dotenv
- jinja2

---

# ▶️ Cómo levantar el proyecto

---

# 🟢 Estado actual del proyecto

✔ Estructura base creada  
✔ docker-compose configurado  
✔ requirements.txt configurado  
✔ Dockerfile creado  
✔ database.py configurado

El proyecto está listo para crear `main.py` y comenzar a generar las tablas.

---

# 🧠 Conceptos aprendidos hasta ahora

## 🔹 Arquitectura base en examen

Separación mínima obligatoria:

- main.py → Punto de entrada
- database.py → Conexión a BD
- Dockerfile → Construcción de la API
- docker-compose.yml → Orquestación
- requirements.txt → Dependencias

---

## 🔹 Conexión en Docker

En Docker NO se usa:

---

# 🟢 API funcionando correctamente

✔ Docker levantado correctamente  
✔ PostgreSQL conectado  
✔ FastAPI funcionando en http://localhost:8000  
✔ Swagger disponible en http://localhost:8000/docs

---

# 🧠 Error común resuelto

Si aparece:

FATAL: password authentication failed

Verificar que:

DATABASE_URL coincida exactamente con:

POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB

Y si se cambian valores:

docker compose down -v
docker compose up --build

---

# 🏗 Modelos creados

## 👨‍🏫 Profesor

Tabla: profesores

Campos:

- id (PK)
- nombre (obligatorio)
- email (único)
- especialidad (opcional)

Relación:
Un profesor puede tener varios alumnos (One-to-Many).

---

## 👨‍🎓 Alumno

Tabla: alumnos

Campos:

- id (PK)
- nombre (obligatorio)
- email (único)
- telefono (opcional)
- profesor_id (ForeignKey → profesores.id)

Relación:
Un alumno pertenece a un profesor.

---

# 🔗 Tipo de relación implementada

Relación bidireccional usando:

- ForeignKey
- relationship
- back_populates

Estructura:

Profesor 1 ---- N Alumno

---

# 🧠 Conceptos clave aprendidos

- **tablename**
- primary_key
- unique
- nullable
- ForeignKey
- relationship
- back_populates
- One-to-Many

---

---

# 📘 Schemas creados

Se han creado schemas para separar:

- Validación de entrada (Create / Update)
- Representación de salida (Response)
- Modelo base reutilizable (Base)

Uso de Pydantic v2:
Se utiliza `from_attributes = True` para compatibilidad con SQLAlchemy.

Separación clara entre:

- Modelo ORM (models/)
- Schema Pydantic (schemas/)

---

# 👨‍🎓 Schema Alumno

Campos:

- id (Response)
- nombre
- email
- telefono (opcional)
- profesor_id (FK opcional)

Se permite:

- Crear alumno con o sin profesor asignado
- Actualizar parcialmente alumno
- Validación automática de email

---

# ⚠️ Nota sobre Docker y PostgreSQL

Es posible que al arrancar el proyecto aparezca temporalmente:

connection refused

Esto ocurre porque la API intenta conectarse antes de que PostgreSQL esté completamente iniciado.

No es un error grave.

Una vez que la base de datos termina de arrancar, la API funciona correctamente.

---

# ⚠️ Nota sobre EmailStr

Para usar EmailStr en Pydantic es necesario instalar:

email-validator

Si no está instalado, FastAPI fallará al arrancar.

---

# 📦 Dependencias del proyecto

El proyecto utiliza:

- FastAPI → Framework principal
- Uvicorn → Servidor ASGI
- SQLAlchemy → ORM
- Psycopg → Conexión PostgreSQL
- Pydantic → Validación de datos
- Email-validator → Soporte para EmailStr
- Jinja2 → Plantillas HTML

---

# ⚠️ Error común en examen

Si se usa EmailStr y no está instalado email-validator:

Aparecerá el error:

ImportError: email-validator is not installed

Solución:
Añadir email-validator en requirements.txt
Reconstruir contenedor con:

docker compose up --build

---

# 🔄 Flujo de un endpoint

1. Llega petición HTTP
2. FastAPI valida datos con Pydantic
3. Se abre sesión con get_db
4. Se consulta o modifica la base de datos
5. Se hace commit si hay cambios
6. Se devuelve respuesta convertida a JSON

---

# 🧠 Diseño de Schemas y Relaciones (Profesor ↔ Alumno)

En este proyecto existe una relación bidireccional entre Profesor y Alumno:

Profesor
└── tiene muchos → Alumnos

Alumno
└── pertenece a → Profesor

## 🚨 Problema: Recursividad infinita

Si en los esquemas Pydantic incluyéramos las relaciones completas en ambos modelos, ocurriría lo siguiente:

ProfesorResponse
└── alumnos: List[AlumnoResponse]

AlumnoResponse
└── profesor: ProfesorResponse

Esto generaría una referencia infinita:

Profesor → Alumno → Profesor → Alumno → Profesor → ...

Lo que provoca:

- Error en Swagger
- Error en Pydantic
- Serialización infinita

---

## ✅ Solución profesional: Schemas "Simple"

Creamos versiones simplificadas de los modelos para usar dentro de relaciones anidadas:

- ProfesorSimple
- AlumnoSimple

Estos esquemas:

- Incluyen solo los campos básicos
- No contienen relaciones internas
- Evitan la recursividad infinita

---

# 📌 Estructura final de Schemas

## 🔹 PROFESOR

### Base

```python
class ProfesorBase(BaseModel):
    nombre: str
    email: EmailStr
    especialidad: Optional[str] = None

Simple (para usar dentro de Alumno)
class ProfesorSimple(ProfesorBase):
    id: int

    class Config:
        from_attributes = True

Response (incluye alumnos)
class ProfesorResponse(ProfesorBase):
    id: int
    alumnos: List[AlumnoSimple] = []

    class Config:
        from_attributes = True

🔹 ALUMNO
Base
class AlumnoBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    profesor_id: Optional[int] = None

Simple (para usar dentro de Profesor)
class AlumnoSimple(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None

    class Config:
        from_attributes = True

Response (incluye profesor)
class AlumnoResponse(AlumnoBase):
    id: int
    profesor: Optional[ProfesorSimple] = None

    class Config:
        from_attributes = True
```
