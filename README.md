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


Esta primera versión, pero la visión real de la plataforma es muchísimo más interactiva. Por pura falta de tiempo antes de la entrega, se quedaron en el tintero varias herramientas que van a transformar por completo cómo se siente usar la aplicación. Esto es lo que le voy a programar para que quede a otro nivel

El temporizador integrado: No quiero depender del reloj del celular ni de otras pestañas. La idea es meterle un timer nativo directamente en la interfaz. para medir los bloques intensivos de estudio, o para los tiempos sin salir del entorno oscuro.

Horario magnético: El sistema actual cumple, pero es muy estático. Lo que voy a construir es un entorno donde cada tarea se sienta como un "imán". Que yo pueda agarrar una tarjeta con el mouse, arrastrarla por la pantalla y que haga snap, tiene que organizarse como un calendario profesional. La meta es poder estirar o encoger los bloques de tiempo gráficamente. que se sienta como google calendar.

Además, quiero meterle comandos rápidos de teclado para registrar todo sin usar el mouse, un "modo de enfoque profundo" que apague el resto de la interfaz para las sesiones de trabajo pesado, y estadísticas avanzadas con mapas de calor para medir mi consistencia. Más adelante, hasta planeo rutear una placa para tener un botón físico en mi escritorio que se conecte directo al sistema, sumarle un algoritmo de repaso espaciado para memorizar los temas de estudio
