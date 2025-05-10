# Repo para EU - DevOps&Cloud - UNIR

Este repositorio incluye un proyecto sencillo para demostrar los conceptos de pruebas unitarias, pruebas de servicio, uso de Wiremock y pruebas de rendimiento
El objetivo es que el alumno entienda estos conceptos, por lo que el código y la estructura del proyecto son especialmente sencillos.
Este proyecto sirve también como fuente de código para el pipeline de Jenkins.

# Calculadora
## Linux
export PYTHONPATH=.

## Windows
SET PYTHONPATH=.

## Ejecutar
python app/calc.py


# Servicio Calculadora
## Linux
export FLASK_APP=app/api.py:api_application

## Windows
SET PALSK_APP=app\api.py:api_application

## Ejecutar
flask run

# Pruebas unitarias
pytest test/unit
pytest test/rest

# wiremock
java -jar wiremock-standalone-2.27.2.jar --port 9090 --root-dir . -v
