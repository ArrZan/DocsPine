from flask import Flask, json, render_template, request, redirect, url_for, send_from_directory
import base64
import os
#import database as db
from datetime import datetime
import shutil  # Módulo para operaciones de sistema de archivos (copiar y eliminar archivos y directorios)
from flask_mysqldb import MySQL

app = Flask(__name__)

db = MySQL(app)

#? ****************************************************************** ?#
#? ************************** VER REGISTRO ************************** ?#
#? ****************************************************************** ?#
""""
@app.route('/')
def litadoTrabajo():
    cursor = db.connection.cursor()
    cursor.execute('''SELECT p.*, u.NombreUsuario FROM Proyectos p
                    JOIN Usuarios u ON p.IDUsuario = u.ID''')
    resultado = cursor.fetchall() # Obtener todos los resultados de la consulta
    nombreColumna = [column[0] for column in cursor.description] # Obtener los nombres de las columnas
    # Convertir cada fila del resultado en un diccionario usando dict(zip())
    objetoProyecto = [dict(zip(nombreColumna, objeto)) for objeto in resultado] 
    
    for proyecto in objetoProyecto:
        imagen_bytes = proyecto['Imagen'] # Obtener los bytes de la imagen
        if imagen_bytes is not None:
            #(base64.b64encode)codifica los bytes de la imagen en base64, que es una forma de representar datos binarios como texto
            proyecto['Imagen'] = base64.b64encode(imagen_bytes).decode('utf-8')
        if isinstance(proyecto['Archivo'], bytes):
            proyecto['Archivo'] = proyecto['Archivo'].decode('utf-8') # Decodificar los bytes de los archivos a una cadena
        proyecto['Archivos'] = proyecto['Archivo'].split(',') # Dividimos la cadena de archivos en una lista de archivos utilizando la coma
    cursor.close()
    return render_template('proyectos/ver_proyecto.html', data=objetoProyecto)

#? ****************************************************************** ?#
#? ************************* VER EL ARCHIVO ************************* ?#
#? ****************************************************************** ?#

# Decorador de Flask que define una nueva ruta en la aplicación web. Cuando un usuario accede a una 
# URL que coincide con este patrón, se ejecuta la función `mostrar_archivo`.
@app.route('/archivo/<nombre_usuario>/<nombre_proyecto>/<nombre_archivo>')
def mostrar_archivo(nombre_usuario, nombre_proyecto, nombre_archivo):
    # Construir la ruta completa del archivo
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario, nombre_proyecto, nombre_archivo)
    print("Ruta del archivo:", ruta_archivo)  # Imprimir la ruta completa del archivo
    # Usar la función `send_from_directory` de Flask para enviar el archivo
    # desde el directorio en el que está almacenado al navegador del usuario.
    return send_from_directory(os.path.dirname(ruta_archivo), nombre_archivo)
"""

#! *********************************************************** *#
#* ************* GUARDAR/REGISTRAR LOS PROYECTOS ************* *#
#! *********************************************************** *#

# Ruta para mostrar el formulario de creación de proyectos
def crear_proyecto():
    # Crear un cursor para ejecutar la consulta
    cursor = db.connection.cursor()
    cursor.execute("SELECT ID, NombreUsuario FROM Usuarios") # Obtener los usuarios y sus IDs
    usuarios = cursor.fetchall() # Obtener todos los resultados de la consulta
    cursor.close()

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('proyectos/crear_proyecto.html', usuarios=usuarios, fecha_actual=fecha_actual)

# Guardar los registros/proyectos
def formAddTrabajo():
    # Obtener la información de cada atributo del formulario
    imagen               = request.files['Imagen'].read() # Leer la imagen del formulario
    nombre_proyecto      = request.form['NombreProyecto']
    descripcion_proyecto = request.form['DescripcionProyecto']
    fecha                = request.form.get('Fecha')
    usuario              = request.form['IDUsuario']
    archivos             = request.files.getlist('Archivo')

    # Verificar que todos los campos necesarios estén presentes
    if nombre_proyecto and descripcion_proyecto and fecha and usuario and archivos:
        cursor = db.connection.cursor()
        cursor.execute("SELECT NombreUsuario FROM Usuarios WHERE ID = %s", (usuario,))
        nombre_usuario = cursor.fetchone()[0] # Obtener el nombre de usuario a partir del ID

        # Construir la ruta de la carpeta del usuario
        carpeta_usuario = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario)
        if not os.path.exists(carpeta_usuario):
            os.makedirs(carpeta_usuario) # Crear la carpeta si no existe

        # Construir la ruta de la carpeta del proyecto
        carpeta_proyecto = os.path.join(carpeta_usuario, nombre_proyecto)
        if not os.path.exists(carpeta_proyecto):
            os.makedirs(carpeta_proyecto) # Crear la carpeta si no existe

        # Guardar cada archivo en la carpeta del proyecto
        nombres_archivos = [] # Lista para almacenar los nombres de los archivos
        contador = 1 # Contador para numerar los archivos
        fecha_hora_actual = datetime.now().strftime('%Y%m%d%H%M%S') # Obtener la fecha y hora actual
        
        for archivo in archivos:
            extension = os.path.splitext(archivo.filename)[1] # Obtener la extensión del archivo
            nombre_archivo = f"{nombre_usuario}({contador})_{fecha_hora_actual}{extension}" # Crear un nombre único para el archivo
            ruta_archivo = os.path.join(carpeta_proyecto, nombre_archivo) # Construir la ruta completa del archivo
            archivo.save(ruta_archivo) # Guardar el archivo en la ruta especificada
            nombres_archivos.append(nombre_archivo) # Agregar el nombre del archivo a la lista
            contador += 1
        # Unir los nombres de los archivos en una cadena separada por comas
        archivos_combinados = ','.join(nombres_archivos)
        
        # Insertar el proyecto en la base de datos
        sql = "INSERT INTO proyectos(Imagen, NombreProyecto, DescripcionProyecto, Fecha, IDUsuario, Archivo) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (imagen, nombre_proyecto, descripcion_proyecto, fecha, usuario, archivos_combinados)
        cursor.execute(sql, data) # Ejecutar la consulta SQL con los datos
        db.database.commit() # Confirmar los cambios en la base de datos
        cursor.close()

    return redirect(url_for('litadoTrabajo')) # Redirigir a la lista de trabajos/proyectos

#! ************************************************************ *#
#* ************* ELIMINAR REGISTRO MEDIANTE EL ID ************* *#
#! ************************************************************ *#
def delete(ID):
    with db.connection.cursor() as cursor:
        # Obtener el nombre del usuario y del proyecto
        cursor.execute("SELECT u.NombreUsuario, p.NombreProyecto, p.Archivo FROM proyectos p JOIN Usuarios u ON p.IDUsuario = u.ID WHERE p.ID = %s", (ID,))
        result = cursor.fetchone()
        if result:
            nombre_usuario, nombre_proyecto, archivos_combinados = result

            # Construir la ruta de la carpeta del proyecto
            carpeta_proyecto = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario, nombre_proyecto)
            
            # Eliminar la carpeta del proyecto y su contenido
            if os.path.exists(carpeta_proyecto):
                shutil.rmtree(carpeta_proyecto)
            
            # Eliminar el registro de la base de datos
            cursor.execute("DELETE FROM proyectos WHERE ID = %s", (ID,))
            db.database.commit()
    
    return redirect(url_for('litadoTrabajo'))

#! ********************************************************** *#
#* ************* EDITAR REGISTRO MEDIANTE EL ID ************* *#
#! ********************************************************** *#
# Ruta para editar un proyecto específico mediante su ID
def editar_proyecto(ID):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM proyectos WHERE ID=%s', (ID,))
    proyecto = cursor.fetchone()
    
    # Obtener el nombre del usuario
    cursor.execute('SELECT NombreUsuario FROM Usuarios WHERE ID=%s', (proyecto[1],))
    nombre_usuario = cursor.fetchone()[0]
    
    # Obtener la lista de archivos asociados al proyecto
    archivos_proyecto = proyecto[5].split(',') if proyecto[5] else []
    
    cursor.close()

    # Convertir la imagen del proyecto a base64 para mostrarla en la interfaz de usuario
    imagen_base64 = base64.b64encode(proyecto[6]).decode('utf-8')

    # Convertir los detalles del proyecto en un diccionario para pasarlos a la plantilla
    proyecto_dict = {
        'ID': proyecto[0],
        'IDUsuario': proyecto[1],
        'NombreProyecto': proyecto[2],
        'DescripcionProyecto': proyecto[3],
        'Fecha': proyecto[4],
        'Archivos': archivos_proyecto,  # Pasar la lista de archivos al template
        'Imagen': imagen_base64,
        'NombreUsuario': nombre_usuario
    }
    return render_template('proyectos/editar_proyecto.html', proyecto=proyecto_dict)

# Ruta para actualizar un proyecto después de la edición

def actualizar_proyecto():
    # Obtener los datos enviados mediante el método POST desde el formulario de edición
    proyecto_id = request.form['ID']
    nombre_proyecto_nuevo = request.form['NombreProyecto']
    descripcion_proyecto_nuevo = request.form['DescripcionProyecto']
    fecha_nueva = request.form['Fecha']
    usuario = request.form['IDUsuario']
    imagen = request.files['Imagen'].read()  # Leer la nueva imagen del formulario
    archivos = request.files.getlist('Archivo') # Obtener la lista de archivos del formulario
    removed_files = json.loads(request.form.get('removedFiles', '[]')) # Obtener la lista de archivos eliminados

    cursor = db.connection.cursor()
    cursor.execute("SELECT u.NombreUsuario FROM Proyectos p JOIN Usuarios u ON p.IDUsuario = u.ID WHERE p.ID = %s", (proyecto_id,))
    nombre_usuario = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM Proyectos WHERE ID = %s", (proyecto_id,))
    proyecto_existente = cursor.fetchone()

    # Verificar si el proyecto existe en la base de datos
    if proyecto_existente:
        nombre_proyecto_anterior = proyecto_existente[2]
        archivos_existentes = proyecto_existente[5].split(',') if proyecto_existente[5] else []
        carpeta_usuario = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario)
        carpeta_proyecto_anterior = os.path.join(carpeta_usuario, nombre_proyecto_anterior)
        carpeta_proyecto_nuevo = os.path.join(carpeta_usuario, nombre_proyecto_nuevo)

        # Eliminar archivos marcados para eliminar de la carpeta del proyecto
        for index in removed_files:
            archivo_a_eliminar = archivos_existentes[index]
            ruta_archivo_a_eliminar = os.path.join(carpeta_proyecto_anterior, archivo_a_eliminar)
            if os.path.exists(ruta_archivo_a_eliminar):
                os.remove(ruta_archivo_a_eliminar)
            # Eliminar el archivo de la lista de archivos existentes
            del archivos_existentes[index]

        # Renombrar la carpeta del proyecto si el nombre del proyecto ha cambiado
        if nombre_proyecto_nuevo != nombre_proyecto_anterior:
            if os.path.exists(carpeta_proyecto_anterior):
                os.rename(carpeta_proyecto_anterior, carpeta_proyecto_nuevo)

        # Crear la carpeta del proyecto si no existe
        if not os.path.exists(carpeta_proyecto_nuevo):
            os.makedirs(carpeta_proyecto_nuevo)

        # Guardar nuevos archivos con el nombre específico
        contador = len(archivos_existentes) + 1  # Iniciar contador desde el número actual de archivos + 1
        fecha_hora_actual = datetime.now().strftime('%Y%m%d%H%M%S')
        for archivo in archivos:
            if archivo.filename:  # Check if file exists
                extension = os.path.splitext(archivo.filename)[1]
                nombre_archivo = f"{nombre_usuario}({contador})_{fecha_hora_actual}{extension}"
                ruta_archivo = os.path.join(carpeta_proyecto_nuevo, nombre_archivo)
                archivo.save(ruta_archivo)
                archivos_existentes.append(nombre_archivo)
                contador += 1

        # Actualizar la imagen del proyecto si se proporcionó una nueva
        if imagen:
            cursor.execute(
                "UPDATE Proyectos SET NombreProyecto = %s, DescripcionProyecto = %s, Fecha = %s, IDUsuario = %s, Imagen = %s, Archivo = %s WHERE ID = %s",
                (nombre_proyecto_nuevo, descripcion_proyecto_nuevo, fecha_nueva, usuario, imagen, ','.join(archivos_existentes), proyecto_id)
            )
        else:
            # Si no se proporcionó una nueva imagen, actualizar el proyecto sin modificar la imagen
            cursor.execute(
                "UPDATE Proyectos SET NombreProyecto = %s, DescripcionProyecto = %s, Fecha = %s, IDUsuario = %s, Archivo = %s WHERE ID = %s",
                (nombre_proyecto_nuevo, descripcion_proyecto_nuevo, fecha_nueva, usuario, ','.join(archivos_existentes), proyecto_id)
            )
        db.database.commit()

    cursor.close()
    return redirect(url_for('litadoTrabajo'))
