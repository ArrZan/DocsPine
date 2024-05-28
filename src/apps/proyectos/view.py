# Importaciones de sistema
import os

# Importaciones de librerías instaladas en env
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Importaciones propias
from config import config

app = Flask(__name__)

db = MySQL(app) # Instancia de mi bd


def listar_proyectos():
    data = {}
    try:
        cursor = db.connection.cursor()
        sql = "select P.IDUsuario, U.ID,U.NombreUsuario, P.NombreProyecto, P.DescripcionProyecto, P.Fecha, P.Imagen from Proyectos P join Usuarios U where P.IDUsuario = U.ID"
        cursor.execute(sql)
        data=cursor.fetchall()
        #print(proyectos)
    except Exception as ex:
        data['mensaje'] = 'Error...'  
    return data 

def listar_mis_proyectos():
    data = {}
    try:
        cursor = db.connection.cursor()
        sql = "select U.NombreUsuario, P.NombreProyecto, P.DescripcionProyecto, P.Fecha, P.Imagen from Proyectos P join Usuarios U where P.IDUsuario = U.ID and P.IDUsuario =%s"
        print(sql)
        cursor.execute(sql,(current_user.id,))
        data=cursor.fetchall()
        print(data)
    except Exception as ex:
        data['mensaje'] = 'Error...'     
    return data