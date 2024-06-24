# Importaciones de sistema
import os

# Importaciones de librerías instaladas en env
from flask import Flask, redirect, request, url_for, render_template, session
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, logout_user, login_required

from Lenguage import Lenguajes
from apps.login.views import LoginView, RegisterView


# Importaciones propias
from apps.user.Models import ModelUser
from apps.user.entities.User import User
from config import config
from apps.proyectos.view import misProyectos, allProyectos, consultProject
from apps.proyectos.view import comentar as proyectos_comentar
from apps.proyectos.view import calificar as proyectos_calificar
from apps.proyectos.view import re_calificar as proyectos_recalificar
from apps.proyectos.view import idioma as select_idioma

# Importaciones para la CRUD de los proyectos/trabajos
from apps.proyectos.view import crear_proyecto as CrearProyect
from apps.proyectos.view import formAddTrabajo as AddTrabajo
from apps.proyectos.view import delete as Eliminar
from apps.proyectos.view import editar_proyecto as EditarP
from apps.proyectos.view import actualizar_proyecto as ActualizarP
from apps.proyectos.view import mostrar_archivo as MostrarArchivo

app = Flask(__name__)

csrf = CSRFProtect() # Protección de csrf pa los form's

socketio = SocketIO(app) # Envío en tiempo real para comentarios


db = MySQL(app) # Instancia de mi bd
login_manager_app = LoginManager(app) 

STATIC_DIR = os.path.join(app.root_path, 'static') # Dirección de mi static

app.static_folder = 'static'

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------------------------------------------------------------------------------------------------------- URLS
app.add_url_rule('/login', view_func=LoginView.as_view('login', db=db))
app.add_url_rule('/register', view_func=RegisterView.as_view('register', db=db, static=STATIC_DIR))


#Funcion para contatar la permanecia de la sesion
@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True


# Ruta logout
# -----------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user_id', None) #Para eliminar el id del usuario del dic de las cookies y tener un logout completo
    logout_user()
    return redirect(url_for('login'))


# Rutas principales una vez logeado
#------------------------------------------------------------

@app.route('/misProyectos', methods=['GET'])
@login_required
def mis_Proyectos():
    order_by = request.args.get('order_by', 'rating_desc')
    return misProyectos(order_by, app.config['PERMANENT_SESSION_LIFETIME'])

@app.route('/List_Proyectos', methods=['GET'])
@login_required
def all_Proyectos():
    order_by = request.args.get('order_by', 'rating_desc')
    return allProyectos(order_by, app.config['PERMANENT_SESSION_LIFETIME'])


# Consulta de un proyecto para mostrar en el modal
@app.route('/publication/<string:id>', methods=['GET'])
@login_required
def consult_project(id):
    return consultProject(id)

#cambio para filtro ---------------


#------------------------------------------------------------
@app.route('/comentar/<string:id>', methods=['POST'])
def comentar(id):
    return proyectos_comentar(id)

@socketio.on('new_comment')
def handle_new_comment(comment):
    # Se difunde el comentario a todos los clientes
    emit('new_comment', comment, broadcast=True)



@app.route('/calificar/<string:id>', methods=['POST'])
def calificar(id):
    return proyectos_calificar(id)

@app.route('/re_calificar/<string:id_pro>/<string:id_ca>', methods=['POST'])
def re_calificar(id_pro,id_ca):
    return proyectos_recalificar(id_pro,id_ca)



@app.route('/idioma/', methods=['POST'])
def idioma():
    return select_idioma()

# !--------------------------- ############################## ---------------------------------
#* RUTAS PARA CREAR PROYECTO/TRABAJOS
# URL que coincide con este patrón, se ejecuta la función `mostrar_archivo`.
@app.route('/archivo/<nombre_usuario>/<nombre_proyecto>/<nombre_archivo>')
def mostrar_archivo(nombre_usuario, nombre_proyecto, nombre_archivo):
    return MostrarArchivo(nombre_usuario, nombre_proyecto, nombre_archivo)

# Ruta para mostrar el formulario de creación de proyectos
@app.route('/crear_proyectos')
@login_required
def crear_proyecto():
    return CrearProyect()

# Guardar los registros/proyectos
@app.route('/registrar', methods=['POST'])
@login_required
def formAddTrabajo():
    return AddTrabajo()

@app.route('/delete/<string:ID>')
@csrf.exempt
def delete(ID):
    return Eliminar(ID)

# Ruta para editar un proyecto específico mediante su ID
@app.route('/editar_proyecto/<string:ID>')
def editar_proyecto(ID):
    return EditarP(ID)
    
# Ruta para actualizar un proyecto después de la edición
@app.route('/actualizar_proyecto', methods=['POST'])
@csrf.exempt
def actualizar_proyecto():
    return ActualizarP()
    

# Errores de respuesta HTTP
#------------------------------------------------------------
def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return render_template('errors/error_404.html'), 404


if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    # Con estas dos líneas controlamos rutas que no existen en nuestra app y 
    # el acceso a rutas protegidas por logeo
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    # Ejecutamos con socketio
    socketio.run(app)

    
