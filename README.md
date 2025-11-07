🧠 Descripción del Sistema de Notas Profesional

El Sistema de Notas Profesional es una aplicación de escritorio desarrollada en Python con la librería Tkinter, que permite gestionar, registrar y analizar las calificaciones de los estudiantes de manera simple y visual.

Su propósito es facilitar el control académico mediante el registro automático en base de datos, la generación de reportes y el análisis gráfico del rendimiento de los alumnos.

⚙️ Características principales

Registro de estudiantes y notas

Permite registrar el nombre del estudiante y tres notas (Nota 1, Nota 2, Nota 3).

Calcula automáticamente el promedio y determina el estado (Aprobado o Desaprobado).

Base de datos integrada

Usa SQLite (notas.db) para almacenar los registros de manera permanente.

Actualiza automáticamente las columnas necesarias si la estructura cambia.

Visualización profesional

Interfaz moderna en tonos oscuros con íconos y botones estilizados.

Tabla interactiva (Treeview) para mostrar los registros con colores:

Azul → Aprobado

Rojo → Desaprobado

Gestión de datos

Buscar y filtrar estudiantes por nombre o estado.

Editar o eliminar registros existentes.

Importar notas desde Excel y exportar datos a Excel con formato profesional (usando Pandas).

Análisis gráfico

Muestra un gráfico de barras con el promedio de cada estudiante (usando Matplotlib).

Incluye una línea de referencia para el promedio mínimo de aprobación (11 puntos).

🗂️ Tecnologías utilizadas

Python 3

Tkinter → interfaz gráfica.

SQLite3 → base de datos local.

Pandas → manejo y exportación de datos.

Matplotlib → generación de gráficos.

🧩 Estructura general del sistema

RegistroNotasApp: clase principal que maneja toda la interfaz y las funciones.

Métodos principales:

registrar(): agrega un nuevo alumno y sus notas.

editar_registro(): permite modificar registros.

eliminar_registro(): borra un estudiante.

filtrar(): busca estudiantes por nombre o estado.

exportar_excel() / importar_excel(): para interoperar con archivos Excel.

ver_grafico(): genera el gráfico de rendimiento.

📈 Ventajas

Todo se guarda automáticamente en una base de datos local.

Puede importar y exportar datos fácilmente.

Posee una interfaz atractiva, moderna y fácil de usar.

Permite analizar visualmente el desempeño académico.

💡 Posibles mejoras futuras

Añadir login de usuario (profesor/administrador).

Integrar envío de reportes por correo electrónico.

Implementar promedios por curso o materia.

Crear versión web o móvil.
