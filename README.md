# Wordplease

Práctica de backend avanzado con Django

## Requisitos

Para poder ejecutar el proyecto correctamente en local, es necesario:

1. Tener un entorno virtual creado.
2. Instalar con *pip install* las depencias del archivo requirements.txt.
3. Tener un base de datos creada junto con un usuario administrador.

## Inicio de la aplicación

Para arrancar el servidor:

1. Activar el entorno virtual *source env/bin/activate*
2. Arrancar el servidor *python manage.py runserver*

## Tareas en background

Celery se encarga de ejecutar tareas en background:

1. Se envía un correo electrónico a los usuarios que han recibido una respuesta mediante la creación de un nuevo post, o que han sido mencionados a través del contenido de un post. Los post solo pueden ser contestados, si el usuario es diferente al que creó el post de manera original. El envío del correo electrónico es real, con lo que puede demorarse unos minutos.

Desde la carpeta del proyecto y en el terminal, ejecuta:

*celery -A wordplease worker* para iniciar celery

Para poder ejecutar estas tareas en background, será necesario tener instalado *rabbitmq* en el equipo.

## Internacionalización
El sitio web esta implementado para soportar los idiomas de español e inglés. La aplicación obtiene el idioma a mostrar a través del navegador web, también se puede cambiar el idioma de la aplicación desde el pie de página.
