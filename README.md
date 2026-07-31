# My Life OS - Habit Tracker

My Life OS es una plataforma web integral diseñada para el seguimiento y la gestión de hábitos personales. Lo hice con un enfoque analítico, permite monitorear rutinas diarias a través de una interfaz de usuario minimalista y en modo oscuro, el objetivo principal es ayudar a las personas a organizarse aun le faltan muchas mejoras y herramientas como la ocion de tener un temporizador para cuando quieras estar en un bloque profundo. No se si ayude a las personas con tdah, pero seguro si a los que les guste organizar todo o los que quieren mejorar su disciplina.

## Que tiene?
* **Gestión de Hábitos:** puedes crear editar y hacer seguimiento de tus rutinas.
* **Interfaz Dark Mode:** Se ve bonito, minimalista y el oscuro le queda bien.
* **Panel de Control (Dashboard):** Ayuda a visualizar el progreso y  el estado de los diferentes hábitos registrados.

## Que use?
* **Backend:** Python y Django (Framework).
* **Despliegue y Producción:** Gunicorn como servidor WSGI y WhiteNoise para la gestión eficiente de archivos estáticos.
* **Infraestructura:** Alojamiento configurado e implementado en Render.


Si quieres tener este proyecto en un entorno de desarrollo local, haz esto:
1. Descarga el repositorio
2. Crea y activa un entorno virtual de Python:
   `python3 -m venv venv`
   `source venv/bin/activate`
3. Instala todas las dependencias necesarias:
   `pip install -r requirements.txt`
4. Aplica las migraciones de la base de datos:
   `python3 manage.py migrate`
5. Levanta el servidor de desarrollo:
   `python3 manage.py runserver`
6. Abre tu navegador y accede a `http://127.0.0.1:8000`.