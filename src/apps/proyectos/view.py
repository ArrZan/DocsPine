import os
import shutil  # Módulo para operaciones de sistema de archivos (copiar y eliminar archivos y directorios)

import base64
from flask import Flask, json, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user


from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from Lenguage import Lenguajes


app = Flask(__name__)

lenguajes=Lenguajes()

csrf = CSRFProtect() # Protección de csrf pa los form's

db = MySQL(app)

# ************************************************************* #
# Configurar la carpeta de carga de archivos
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'archivos_cargados'))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Configurar la carpeta de carga en la aplicación Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configurar el LoginManager para manejar sesiones de usuario
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------


def get_base_query2():
    return (
    'SELECT p.ID, p.IDUsuario, p.NombreProyecto, p.DescripcionProyecto, p.Fecha, p.Imagen, Usuarios.Foto, Usuarios.NombreUsuario AS NombreUsuario, '
    'IFNULL(AVG(Calificacion.Calificacion), 0) AS PromedioCalificacion '
    'FROM Proyectos p '
    'JOIN Usuarios ON p.IDUsuario = Usuarios.ID '
    'LEFT JOIN Calificacion ON p.ID = Calificacion.IDProyecto '
    )

def order_base(order_by, base):

    if order_by == 'rating_asc':
        base += 'ORDER BY PromedioCalificacion ASC'
    elif order_by == 'rating_desc':
        base += 'ORDER BY PromedioCalificacion DESC'
    else:
        base += 'ORDER BY RAND()'  # Ordenamiento aleatorio

    return base


def getLanguajeSystem():
    if 1==current_user.idioma:
        i=lenguajes.Español()
    if 2==current_user.idioma:
        i=lenguajes.Ingles()
    if 3==current_user.idioma:
        i=lenguajes.Frances()
    if 4==current_user.idioma:
        i=lenguajes.Italiano()
    if 5==current_user.idioma:
        i=lenguajes.Portugues()
    if 6==current_user.idioma:
        i=lenguajes.Alemán()
    if 7==current_user.idioma:
        i=lenguajes.Polaco()
    if 8==current_user.idioma:
        i=lenguajes.Ruso()

    return i

def structure_data_Projects(objetoProyecto):
    for proyecto in objetoProyecto:
        # Convierte la imagen en un formato correcto para enviar una cadena base64 válida
        if 'Imagen' in proyecto:
            proyecto['Imagen'] = convert_image_base64(proyecto['Imagen'])

        if isinstance(proyecto['Archivo'], bytes):
                proyecto['Archivo'] = proyecto['Archivo'].decode('utf-8') # Decodificar los bytes de los archivos a una cadena

        if 'Archivo' in proyecto:
            # Pregunta si existen archivos y los separa
            if proyecto['Archivo'] is not None:
                proyecto['Archivos'] = proyecto['Archivo'].split(',') # Dividimos la cadena de archivos en una lista de archivos utilizando la coma
            else:
                proyecto['Archivo'] = 'none'


        # Pregunta si existe foto y construye la ruta
        if 'foto' in proyecto:
            proyecto['Foto'] = get_photo_perfil(proyecto['Foto'])

    return objetoProyecto

def structure_data_ProjectPersonal(objetoProyecto):
    for proyecto in objetoProyecto:
        # Convierte la imagen en un formato correcto para enviar una cadena base64 válida
        if 'Imagen' in proyecto:
            proyecto['Imagen'] = convert_image_base64(proyecto['Imagen'])

        # Pregunta si existe foto y construye la ruta
        proyecto['Foto'] = get_photo_perfil(proyecto['Foto'])

    return objetoProyecto


def convert_image_base64(byte_image):
    if byte_image is not None:
        #(base64.b64encode)codifica los bytes de la imagen en base64, que es una forma de representar datos binarios como texto
        return base64.b64encode(byte_image).decode('utf-8')


def get_image_comment(objetoComentarios):
    for comentario in objetoComentarios:
        comentario['Foto'] = get_photo_perfil(comentario['Foto'])

    return objetoComentarios


def extract_info_query(query, param=None):
    cursor = db.connection.cursor()
    if param:
        cursor.execute(query, param)
    else:
        cursor.execute(query)

    resultado = cursor.fetchall()

    nameColumn = [column[0] for column in cursor.description]

    cursor.close()

    return [dict(zip(nameColumn, objeto)) for objeto in resultado]


def extract_dataUser_comments(query, param):
    cursor = db.connection.cursor()
    cursor.execute(query, param)

    columns = cursor.fetchall()

    cursor.close()

    # Devolvemos un  diccionario con las claves del id [0] de los usuarios
    # con el nombre [1] y su foto [2]
    return {row[0]: {'name': row[1], 'photo': get_photo_perfil(row[2]),} for row in columns}


def get_photo_perfil(str_foto):
    if str_foto:
        return f'static/img/perfil/{str_foto}'
    else:
        return f'static/img/perfil/default.jpg'










#* ********************************************************************************************* *#
# COMENTAR
#* ********************************************************************************************* *#

def save_comment(id_project, comentario):

    fecha = datetime.now()

    formatedDate = fecha.strftime('%Y-%m-%d %H:%M:%S')

    cursor = db.connection.cursor()
    sql = "INSERT INTO Comentarios (IDProyecto,IDUsuario, Comentario, Fecha) VALUES (%s, %s, %s, %s)"
    data = (id_project, current_user.id, comentario, formatedDate)

    cursor.execute(sql, data)
    db.connection.commit()

    return {
        'NombreUsuario': current_user.username,
        'Foto': current_user.get_image(),
        'comentario': comentario,
        'fecha': fecha.strftime('%Y-%m-%d / %H:%M:%S')
    }


def comentar(id_project):
    redactar_comentario = request.form['redactar_comentario']

    if redactar_comentario:

        coment_response = save_comment(id_project, redactar_comentario)

        # socketio.emit('new_comment', coment_response, broadcast=True, include_self=False)

        return jsonify({'new_comment': coment_response, 'id_issuer': current_user.id})

    else:
        return jsonify({'error': 'El comentario está vacío'}), 400




#* ********************************************************************************************* *#
# CALIFICAR
#* ********************************************************************************************* *#

def calificar(id):

    try:
        calificar_proyecto = request.form['estrellas' + id]

        # Resto del código
        if calificar_proyecto:
            cursor = db.connection.cursor()
            sql = "INSERT INTO Calificacion (IDProyecto,IDUsuario, Calificacion) VALUES (%s, %s, %s)"
            data = (id, current_user.id, calificar_proyecto)
            cursor.execute(sql, data)
            db.connection.commit()
    except KeyError:
        print('La clave esperada no está presente en el formulario')

    return redirect(url_for('all_Proyectos'))




#* ********************************************************************************************* *#
# RE CALIFICAR
#* ********************************************************************************************* *#

def re_calificar(id_pro,id_ca):

    try:
        calificar_proyecto = request.form['estrellas' + id_pro]
        print('Calificar proyecto:', calificar_proyecto)

        # Resto del código
        if calificar_proyecto:
            cursor = db.connection.cursor()
            sql = "UPDATE Calificacion SET IDProyecto = %s, IDUsuario= %s, Calificacion = %s WHERE ID = %s"
            data = (id_pro, current_user.id, calificar_proyecto,id_ca)
            cursor.execute(sql, data)
            db.connection.commit()
    except KeyError:
        print('La clave esperada no está presente en el formulario')

    return redirect(url_for('all_Proyectos'))




#* ********************************************************************************************* *#
# IDIOMA
#* ********************************************************************************************* *#

def idioma():
    idioma_select = request.form['idioma']
    print('Idioma seleccionado', idioma_select)

    if idioma:
        cursor = db.connection.cursor()
        sql = "UPDATE Usuarios SET IDLenguaje = %s WHERE ID = %s"
        data = (idioma_select,current_user.id)
        cursor.execute(sql, data)
        db.connection.commit()

    return redirect(url_for('all_Proyectos'))



#* ********************************************************************************************* *#
# PROYECTOS PERSONALES
#* ********************************************************************************************* *#

def misProyectos(order_by='random', sessionTime=0):

    # Query del projects
    base_query = get_base_query2() + ('WHERE p.IDUsuario = %s '
                                    'GROUP BY p.ID, Usuarios.NombreUsuario ')

    base_query = order_base(order_by, base_query)

    # Proceso para obtener la lista de los proyectos
    objetoProyecto = structure_data_ProjectPersonal(extract_info_query(base_query, (current_user.id, )))

    # # Proceso para definir el idioma del sistema
    idioma = getLanguajeSystem()

    return render_template('proyectos/misProyectosPrueba.html',
                        idioma=idioma,
                        proyectos=objetoProyecto,
                        # comentarios=objetoComentarios,
                        # calificacion=objetoCalificacion,
                        idUsuariologin=current_user.id,
                        sessionTime=sessionTime)



#* ********************************************************************************************* *#
# LISTA DE TODOS LOS PROYECTOS
#* ********************************************************************************************* *#

def allProyectos(order_by='random', sessionTime=0):

    #Para poder usar el filtro cambio 15-06-24
    base_query = get_base_query2() + 'GROUP BY p.ID, Usuarios.NombreUsuario '

    base_query = order_base(order_by, base_query)

    # Proceso para obtener la lista de los proyectos
    objetoProyecto = structure_data_ProjectPersonal(extract_info_query(base_query))

    # # Proceso para definir el idioma del sistema
    idioma = getLanguajeSystem()

    return render_template('proyectos/prueba.html',
                        idioma=idioma,
                        proyectos=objetoProyecto,
                    #    comentarios=objetoComentarios,
                    #    calificacion=objetoCalificacion,
                        idUsuariologin=current_user.id,
                        sessionTime=sessionTime)



#* ********************************************************************************************* *#
# LISTA DE TODOS LOS PROYECTOS
#* ********************************************************************************************* *#


def consultProject(id_project):
    try:

        query_project = (
            'SELECT DescripcionProyecto, Fecha, Archivo '
            'FROM Proyectos '
            'WHERE Proyectos.ID = %s '
        )

        query_comments = (
            'SELECT IDUsuario, Comentario, Fecha '
            'FROM Comentarios C '
            'WHERE IDProyecto = %s '
            'ORDER BY Fecha desc '
            )

        query_comments_user = (
            'SELECT DISTINCT C.IDUsuario, U.NombreUsuario AS NombreUsuario, U.Foto '
            'FROM Comentarios C, Usuarios U '
            'WHERE C.IDUsuario = U.ID '
            'AND IDProyecto = %s '
        )

        query_rating_user =  (
            'SELECT ID, Calificacion '
            'FROM Calificacion C '
            'WHERE IDProyecto = %s '
            'AND C.IDUsuario = %s '
        )

        # Proceso para obtener el proyecto
        objetoProyecto = structure_data_Projects(extract_info_query(query_project, (id_project, )))

        if not objetoProyecto[0]['Archivos'][0]:
            objetoProyecto[0]['Archivos'] = 0

        # Proceso para obtener la lista de los comentarios de un proyecto
        objetoComentarios = extract_info_query(query_comments, (id_project, ))

        # Proceso para obtener info de los usuarios que comentaron un proyecto
        users = extract_dataUser_comments(query_comments_user, (id_project, ))

        # Proceso para obtener la lista de los calificacion
        rating = extract_info_query(query_rating_user, (id_project, current_user.id,))

        return jsonify({'message': 'Respuesta recibida',
                        'proyecto': objetoProyecto,
                        'comentarios': objetoComentarios,
                        'users': users,
                        'rating': rating,
                        })

    except Exception as e:
        print('Ocurrió un error: ', e)
        return jsonify({'error': 'Hubo un error en la solicitud'})













#? ****************************************************************** ?#
#? ************************* VER EL ARCHIVO ************************* ?#
#? ****************************************************************** ?#

# Decorador de Flask que define una nueva ruta en la aplicación web. Cuando un usuario accede a una
# URL que coincide con este patrón, se ejecuta la función `mostrar_archivo`.

def mostrar_archivo(nombre_usuario, nombre_proyecto, nombre_archivo):
    # Construir la ruta completa del archivo
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario, nombre_proyecto, nombre_archivo)
    # Usar la función `send_from_directory` de Flask para enviar el archivo
    # desde el directorio en el que está almacenado al navegador del usuario.
    return send_from_directory(os.path.dirname(ruta_archivo), nombre_archivo)

#! *********************************************************** *#
#* ************* GUARDAR/REGISTRAR LOS PROYECTOS ************* *#
#! *********************************************************** *#

# Ruta para mostrar el formulario de creación de proyectos
def crear_proyecto():
    # Obtener todos los usuarios para el formulario
    cursor = db.connection.cursor()
    cursor.execute("SELECT ID, NombreUsuario FROM Usuarios") # Obtener los usuarios y sus IDs
    usuarios = cursor.fetchall() # Obtener todos los resultados de la consulta
    cursor.close()

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    idioma = getLanguajeSystem()

    return render_template('proyectos/crear_proyecto.html',idioma=idioma, usuarios=usuarios, fecha_actual=fecha_actual, usuario_actual=current_user.username)

# Guardar los registros/proyectos
def formAddTrabajo():
    # Obtener la información de cada atributo del formulario
    imagen               = request.files['Imagen'].read() # Leer la imagen del formulario
    nombre_proyecto      = request.form['NombreProyecto']
    descripcion_proyecto = request.form['DescripcionProyecto']
    fecha                = request.form['Fecha']
    usuario              = current_user.id  # Obtener el ID del usuario actual
    archivos             = request.files.getlist('Archivo')

    # Verificar que todos los campos necesarios estén presentes
    if nombre_proyecto and descripcion_proyecto and fecha and usuario and archivos:
        cursor = db.connection.cursor()
        cursor.execute("SELECT NombreUsuario FROM Usuarios WHERE ID = %s", (usuario,))
        nombre_usuario = cursor.fetchone()[0]  # Obtener el nombre de usuario a partir del ID
        cursor.close()

        # Construir la ruta de la carpeta del usuario
        carpeta_usuario = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario)
        if not os.path.exists(carpeta_usuario):
            os.makedirs(carpeta_usuario)  # Crear la carpeta si no existe

        # Construir la ruta de la carpeta del proyecto
        carpeta_proyecto = os.path.join(carpeta_usuario, nombre_proyecto)
        if not os.path.exists(carpeta_proyecto):
            os.makedirs(carpeta_proyecto)  # Crear la carpeta si no existe

        try:
            # Guardar cada archivo en la carpeta del proyecto
            nombres_archivos = []
            contador = 1
            fecha_hora_actual = datetime.now().strftime('%Y%m%d%H%M%S')

            for archivo in archivos:
                extension = os.path.splitext(archivo.filename)[1]
                nombre_archivo = f"{nombre_usuario}({contador})_{fecha_hora_actual}{extension}"
                ruta_archivo = os.path.join(carpeta_proyecto, nombre_archivo)
                archivo.save(ruta_archivo)
                nombres_archivos.append(nombre_archivo)
                contador += 1

            # Unir los nombres de los archivos en una cadena separada por comas
            archivos_combinados = ','.join(nombres_archivos)

            # Insertar el proyecto en la base de datos
            cursor = db.connection.cursor()
            sql = "INSERT INTO Proyectos (Imagen, NombreProyecto, DescripcionProyecto, Fecha, IDUsuario, Archivo) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (imagen, nombre_proyecto, descripcion_proyecto, fecha, usuario, archivos_combinados)
            cursor.execute(sql, data)
            db.connection.commit()
            cursor.close()

        except Exception as e:
            flash(f"Error al guardar archivos: {str(e)}", "error")
            return redirect(url_for('crear_proyecto'))

    return redirect(url_for('mis_Proyectos'))

#! ************************************************************ *#
#* ************* ELIMINAR REGISTRO MEDIANTE EL ID ************* *#
#! ************************************************************ *#
def delete(ID):
    with db.connection.cursor() as cursor:
        # Verificar si hay comentarios relacionados y eliminarlos
        cursor.execute("SELECT ID FROM Comentarios WHERE IDProyecto = %s", (ID,))
        comentarios_ids = cursor.fetchall()

        for comentario_id in comentarios_ids:
            cursor.execute("DELETE FROM Comentarios WHERE ID = %s", (comentario_id,))

        # Verificar si hay calificaciones relacionadas y eliminarlas
        cursor.execute("SELECT ID FROM Calificacion WHERE IDProyecto = %s", (ID,))
        calificaciones_ids = cursor.fetchall()

        for calificacion_id in calificaciones_ids:
            cursor.execute("DELETE FROM Calificacion WHERE ID = %s", (calificacion_id,))

        # Obtener la información del proyecto antes de eliminarlo
        cursor.execute("SELECT u.NombreUsuario, p.NombreProyecto, p.Archivo FROM Proyectos p JOIN Usuarios u ON p.IDUsuario = u.ID WHERE p.ID = %s", (ID,))
        result = cursor.fetchone()

        if result:
            nombre_usuario, nombre_proyecto, archivos_combinados = result

            # Construir la ruta de la carpeta del proyecto
            carpeta_proyecto = os.path.join(app.config['UPLOAD_FOLDER'], nombre_usuario, nombre_proyecto)

            # Eliminar la carpeta del proyecto y su contenido
            if os.path.exists(carpeta_proyecto):
                shutil.rmtree(carpeta_proyecto)

            # Eliminar el registro del proyecto en la base de datos
            cursor.execute("DELETE FROM Proyectos WHERE ID = %s", (ID,))
            db.connection.commit()

            # flash(f"El proyecto '{nombre_proyecto}' y sus comentarios/calificaciones han sido eliminados correctamente.", "success")
        else:
            flash("No se encontró el proyecto especificado.", "error")

    return redirect(url_for('mis_Proyectos'))


#! ********************************************************** *#
#* ************* EDITAR REGISTRO MEDIANTE EL ID ************* *#
#! ********************************************************** *#
# Ruta para editar un proyecto específico mediante su ID
def editar_proyecto(ID):
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM Proyectos WHERE ID=%s', (ID,))
    proyecto = cursor.fetchone()

    # Obtener el nombre del usuario
    cursor.execute('SELECT NombreUsuario FROM Usuarios WHERE ID=%s', (proyecto[1],))
    nombre_usuario = cursor.fetchone()[0]

    # Obtener la lista de archivos asociados al proyecto
    archivos_proyecto = proyecto[5].split(',') if proyecto[5] else []

    cursor.close()

    # Convertir la imagen del proyecto a base64 para mostrarla en la interfaz de usuario
    if proyecto[6] is not None:
        imagen_base64 = base64.b64encode(proyecto[6]).decode('utf-8')
    else:
        imagen_base64 = url_for('static', filename='img/perfil/default.jpg')
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
    # Proceso para definir el idioma del sistema
    idioma = getLanguajeSystem()

    return render_template('proyectos/editar_proyecto.html', idioma=idioma, proyecto=proyecto_dict)

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
        if removed_files:
            # Ordenar índices en orden descendente para eliminar correctamente
            removed_files.sort(reverse=True)
            for index in removed_files:
                if index < len(archivos_existentes):
                    print(index)
                    print(archivos_existentes)
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
        db.connection.commit()

    cursor.close()
    return redirect(url_for('mis_Proyectos'))
