# ==========================================================
# 🔹 IMPORTACIONES PRINCIPALES DE FASTAPI
# ==========================================================

from fastapi import FastAPI
# Importamos la clase principal FastAPI.
# Es el núcleo de la aplicación.
# Con ella creamos la instancia "app" que representa nuestra API.


from fastapi.templating import Jinja2Templates
# Importamos el sistema de plantillas Jinja2.
# Permite renderizar HTML dinámico en lugar de devolver solo JSON.
# Se usa para construir páginas web (frontend) desde el backend.


from fastapi.staticfiles import StaticFiles
# Permite servir archivos estáticos como:
# - CSS
# - JavaScript
# - Imágenes
# - Archivos multimedia
# Sin esto, el navegador no podría cargar estilos ni scripts.


from fastapi import Request
# Representa la petición HTTP del cliente.
# Es obligatorio cuando usamos Jinja2Templates.
# Se pasa al HTML para que la plantilla tenga acceso a:
# - URL actual
# - Datos de la petición
# - Información del usuario (si hubiera autenticación)


# ==========================================================
# 🔹 IMPORTACIONES DE BASE DE DATOS
# ==========================================================

from app.database import engine, Base
# engine → conexión con la base de datos.
# Base → clase base de SQLAlchemy que registra todos los modelos.
# Se usa para crear automáticamente las tablas con Base.metadata.create_all().


# ==========================================================
# 🔹 IMPORTACIÓN DE MODELOS (IMPORTANTE)
# ==========================================================

from app.models.profesor import Profesor
# Importamos el modelo Profesor.
# Esto es necesario para que SQLAlchemy lo registre
# y pueda crear su tabla en la base de datos.


from app.models.alumno import Alumno
# Importamos el modelo Alumno.
# Igual que Profesor, es obligatorio importarlo
# para que se cree su tabla al iniciar la aplicación.


# ==========================================================
# 🔹 IMPORTACIÓN DE ROUTERS
# ==========================================================

from app.routers import profesor
# Importamos el router que contiene
# todos los endpoints relacionados con Profesores.


from app.routers import alumno
# Importamos el router que contiene
# todos los endpoints relacionados con Alumnos.


# Creamos la aplicación FastAPI.

app = FastAPI(
    title="Gimnasio Apolo API",
    description="API para gestionar el gimnasio Apolo, incluyendo clientes, entrenadores, clases y horarios.",
    version="1.0.0"   
)

# ==========================================================
# 🔹 CONFIGURACIÓN DE PLANTILLAS (HTML)
# ==========================================================

templates = Jinja2Templates(directory="app/templates")
# Indicamos dónde están las plantillas HTML.
# En este caso:
# app/templates/
# Aquí estará nuestro index.html, login.html, etc.


# ==========================================================
# 🔹 CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# ==========================================================

app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Montamos la carpeta static para poder usar:
# - CSS
# - JS
# - Imágenes
#
# URL pública será:
# http://localhost:8000/static/...
#
# Ejemplo:
# <link rel="stylesheet" href="/static/css/style.css">


# Incluimos el router del profesor en la aplicación.
app.include_router(profesor.router) 

# Incluimos el router del alumno en la aplicación.
app.include_router(alumno.router)
 
# Crear tablas automaticamente al iniciar la aplicación.
Base.metadata.create_all(bind=engine)

# Rutas y lógica de la aplicación se agregarán aquí en el futuro.
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ==========================================================
# 🔹 RUTA PRINCIPAL WEB
# ==========================================================

@app.get("/")
def home(request: Request):
    """
    Renderiza la página principal (index.html).
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
