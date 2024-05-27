# Importaciones de sistema
import os

# Importaciones de librerías instaladas en env
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from apps.login.views import LoginView, RegisterView
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from apps.project.views import home as proyectos_home
from apps.project.views import comentar as proyectos_comentar
from apps.project.views import calificar as proyectos_calificar
from apps.project.views import re_calificar as proyectos_recalificar
from apps.project.views import idioma as select_idioma
# Importaciones propias
from apps.user.Models import ModelUser
from apps.user.entities.User import User

from config import config

app = Flask(__name__)

csrf = CSRFProtect() # Protección de csrf pa los form's
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


# Ruta logout
# -----------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Rutas principales una vez logeado
#------------------------------------------------------------
@app.route('/home')
@login_required
def home():
    return proyectos_home()

#------------------------------------------------------------
@app.route('/comentar/<string:id>', methods=['POST'])
def comentar(id):
    return proyectos_comentar(id)

@app.route('/calificar/<string:id>', methods=['POST'])
def calificar(id):
    return proyectos_calificar(id)

@app.route('/re_calificar/<string:id_pro>/<string:id_ca>', methods=['POST'])
def re_calificar(id_pro,id_ca):
    return proyectos_recalificar(id_pro,id_ca)

@app.route('/idioma/', methods=['POST'])
def idioma():
    return select_idioma()

#------------------------------------------------------------


@app.route('/mis-proyectos')
@login_required
def misProyectos():
    return render_template('proyectos/misProyectos.html')

# Errores de respuesta HTTP
#------------------------------------------------------------
def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '<h1>Página no encontrada</h1>', 404


if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    # Con estas dos líneas controlamos rutas que no existen en nuestra app y 
    # el acceso a rutas protegidas por logeo
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
