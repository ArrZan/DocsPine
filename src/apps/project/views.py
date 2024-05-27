import base64
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user

import base64

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from Lenguage import Lenguajes

lenguajes=Lenguajes()

from apps.user.Models import ModelUser
app = Flask(__name__)

csrf = CSRFProtect() # Protección de csrf pa los form's
db = MySQL(app)

def home():


    # print(current_user.id)
    # print(current_user.username)
    # print(current_user.password)
    # print(current_user.fullname)
    # print(current_user.email)
    # print(current_user.idioma)
    cursor = db.connection.cursor()
    # proceso para obtener la lista de los proyectos
    cursor.execute(
        'SELECT proyectos.*, usuarios.NombreUsuario AS NombreUsuario FROM proyectos, usuarios WHERE proyectos.IDUsuario = usuarios.ID')
    resultado = cursor.fetchall()
    nombreColumna = [column[0] for column in cursor.description]
    objetoProyecto = [dict(zip(nombreColumna, objeto)) for objeto in resultado]
    #combierte la imagen en un formato correcto para enviar un cadena base64 válida.
    for proyecto in objetoProyecto:
        imagen_bytes = proyecto['Imagen']
        proyecto['Imagen'] = base64.b64encode(imagen_bytes).decode('utf-8')

    # Proceso para obtener la lista de los comentarios
    cursor.execute(
        'SELECT comentarios.*, usuarios.NombreUsuario AS NombreUsuario FROM comentarios, usuarios WHERE  comentarios.IDUsuario = usuarios.ID')
    resultado = cursor.fetchall()
    nombreColumnaComentarios = [column[0] for column in cursor.description]
    objetoComentarios = [dict(zip(nombreColumnaComentarios, objeto)) for objeto in resultado]
    # for comentario in objetoComentarios:
    #     imagen_bytes = comentario['Foto_perfil']
    #     comentario['Foto_perfil'] = base64.b64encode(imagen_bytes).decode('utf-8')

    # Proceso para obtener la lista de los idiomas
    cursor.execute(
        'SELECT * FROM lenguaje')
    resultado = cursor.fetchall()
    nombreColumnaIdioma = [column[0] for column in cursor.description]
    objetoLenguaje = [dict(zip(nombreColumnaIdioma, objeto)) for objeto in resultado]
    # Proceso para obtener la lista de los calificacion
    cursor.execute(
        'SELECT * FROM calificacion')
    resultado = cursor.fetchall()
    nombreColumnaCalificacion = [column[0] for column in cursor.description]
    objetoCalificacion = [dict(zip(nombreColumnaCalificacion, objeto)) for objeto in resultado]

    cursor.close()

    # # Proceso para definir el idioma del sistema
    idioma=[]

    if 1==current_user.idioma:
        i=lenguajes.Español()
        idioma=i
        print(idioma)
    if 2==current_user.idioma:
        i=lenguajes.Ingles()
        idioma=i
        print(idioma)
    if 3==current_user.idioma:
        i=lenguajes.Frances()
        idioma=i
        print(idioma)
    if 4==current_user.idioma:
        i=lenguajes.Italiano()
        idioma=i
        print(idioma)
    if 5==current_user.idioma:
        i=lenguajes.Portugues()
        idioma=i
    print(current_user.idioma)
    return render_template('proyectos/home.html',idioma=idioma, proyectos=objetoProyecto, comentarios=objetoComentarios, calificacion=objetoCalificacion, idUsuariologin=current_user.id)

def comentar(id):
    redactar_comentario = request.form['redactar_comentario']
    fecha=datetime.now()
    # print(current_user.id)
    # print(id)

    if redactar_comentario:
        cursor = db.connection.cursor()
        sql = "INSERT INTO comentarios (IDProyecto,IDUsuario, Comentario, Fecha) VALUES (%s, %s, %s, %s)"
        data = (id, current_user.id, redactar_comentario,fecha)
        cursor.execute(sql, data)
        db.connection.commit()

    return redirect(url_for('home'))

def calificar(id):
    # Imprimir el valor de id para verificar que sea correcto
    print('Valor de id:', id)

    # Imprimir request.form completo para ver qué claves están presentes
    print('Datos del formulario:', request.form)

    try:
        calificar_proyecto = request.form['estrellas' + id]
        print('Calificar proyecto:', calificar_proyecto)

        # Resto del código
        if calificar_proyecto:
            cursor = db.connection.cursor()
            sql = "INSERT INTO calificacion (IDProyecto,IDUsuario, Calificacion) VALUES (%s, %s, %s)"
            data = (id, current_user.id, calificar_proyecto)
            cursor.execute(sql, data)
            db.connection.commit()
    except KeyError:
        print('La clave esperada no está presente en el formulario')

    return redirect(url_for('home'))

def re_calificar(id_pro,id_ca):
    # Imprimir el valor de id para verificar que sea correcto
    print('Valor de id:', id_pro)

    # Imprimir request.form completo para ver qué claves están presentes
    print('Datos del formulario:', request.form)

    try:
        calificar_proyecto = request.form['estrellas' + id_pro]
        print('Calificar proyecto:', calificar_proyecto)

        # Resto del código
        if calificar_proyecto:
            cursor = db.connection.cursor()
            sql = "UPDATE calificacion SET IDProyecto = %s, IDUsuario= %s, Calificacion = %s WHERE ID = %s"
            data = (id_pro, current_user.id, calificar_proyecto,id_ca)
            cursor.execute(sql, data)
            db.connection.commit()
    except KeyError:
        print('La clave esperada no está presente en el formulario')

    return redirect(url_for('home'))


def idioma():
    idioma_select = request.form['idioma']
    print('Idioma seleccionado', idioma_select)

    if idioma:
        cursor = db.connection.cursor()
        sql = "UPDATE usuarios SET IDLenguaje = %s WHERE ID = %s"
        data = (idioma_select,current_user.id)
        cursor.execute(sql, data)
        db.connection.commit()

    return redirect(url_for('home'))