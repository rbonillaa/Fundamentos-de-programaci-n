# ESPOL - Fundamentos de Programación


## Script de validación de datos
Este script le servirá a cada profesor de Fundamentos de Programaciòn para validar el formato de los datos que se solicitan al finalizar el semestre. 

El script deberá variar para cada semestre según las ponderaciones de los temas de los examenes, proyectos y sustentaciones. 

**Datos a validar:**

* Nombre
* Matricula
* Genero
* Paralelo
* cod_carrera
* veces_tomadas
* 1er_proyecto
* 1er_sustent
* 1er_lecciones
* 1er_calif\_final
* 1er_exam\_tema1
* 1er_exam\_tema2
* 1er_exam\_tema3
* 1er_exam\_tema4
* 2do_proyecto
* 2do_sustent
* 2do_lecciones
* 2do_calif\_final
* 2do_exam\_tema1
* 2do_exam\_tema2
* 2do_exam\_tema3
* calif_final\_practica
* 3er_proyecto
* 3er_calif\_final
* 3er_exam\_tema1
* 3er_exam\_tema2
* 3er_exam\_tema3

**Validaciones implementadas**

| Tipo de error    | Color    | Soluciona | Comentarios |
| ---------------  |----------| :------:| ----------------|
| Vacio            | Naranja  |         | Los datos básicos (Nombre, paralelo, ...) no deben estar vacios |
| Opción no valida | Azul     |         | Las celdas género y veces_tomadas deben estar entre los valores posibles |
| Fuera de rango   | Amarillo |         | La calificación debe estar dentro del rango posible |
| Tipo no numérico | Verde    |  X     | Todas las calificacoines deben ser entero o float |
| No redondeado    | Rosado   |  X     | Esto aplica para las calificaciones finales(El script lo corrige) |

## Dependencias

Instalar el siguiente paquete de python:

* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)

## Uso

* Llene el arhivo de excel src/archivo.xlsx
* Puede cambiar el nombre del archivo
* Ejecute el script como: **python3 src/validation_data.py archivo.xlsx**
* Al finalizar se imprimirá un mensaje con la cantidad de estudiantes en los que se encontraron errores.
* Abra su archivo y corrija las celdas con los colores descritos en la tabla descrita anterior.
* Vuelva a correr el script.

====================================

© 2018 eslozano, obayona