import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from flask.views import MethodView
from werkzeug.utils import secure_filename

from flask_login import login_user, current_user

# 
# ------------------------------------------------------------------------------------------------------------- Modelos
from apps.user.Models import ModelUser
from apps.user.entities.User import User

from apps.user.utils import generateRandomName
# --------------------------------------------------------------------------------------------------------------- Login
class LoginView(MethodView):
    def __init__(self, db):
        self.db = db
    
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('auth/login.html')
    
    def post(self):
        #Primero preguntamos si el usuario ya se ha autenticado
        if current_user.is_authenticated:
            # Si ya está, se lo devuelve al home
            return redirect(url_for('home'))
        
        # Creamos el objeto usuario con los datos enviados del POST
        user = User(0, request.form['username'], request.form['password'])

        # Mandamos a verificar si existe y si me devuelve las claves correctas
        logged_user = ModelUser.login(self.db, user)

        if logged_user != None:
            # Preguntamos si la contraseña es la correcta (True)
            if logged_user.password:
                # Almacenamos el usuario logeado
                login_user(logged_user)
                # Lo redireccionamos a home ya que se ha logeado
                return redirect(url_for('home'))
            else:
                print("La clave no es la correcta")
                flash("La clave no es la correcta.")
                return render_template('auth/login.html')
        else:
            print("Usuario no encontrado")
            flash('Usuario no encontrado.')
            return render_template('auth/login.html')
        
        return render_template('auth/login.html')


# ------------------------------------------------------------------------------------------------------- Ruta Register
class RegisterView(MethodView):
    def __init__(self, db, static):
        self.db = db
        self.static = static
    
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('auth/login.html')
    
    def post(self):
        # Creamos el objeto usuario con los datos enviados del POST
        try:
            username = request.form['username1']
            fullname = request.form['fullname']
            email = request.form['email']
            password = request.form['password']
            idioma = request.form['idioma']

            # Comprobamos si hay imagen guardada
            if 'image' in request.files:
                image = request.files['image']
                # Si hay nombre de imagen
                if image.filename != '':
                    # Generamos un nombre aleatorio con su debido formato
                    randomName = generateRandomName(name=image.filename)
                    if randomName != None:
                        # Generamos un nombre más seguro
                        filename = secure_filename(randomName)

                        image_dir = os.path.join(self.static, 'images', 'perfil')

                        # Guardamos la imagen en la dirección 'static/images/perfil' con el nombre seguro
                        image.save(os.path.join(image_dir, filename))
            else:
                filename = ''

            # Instanciamos los datos
            user = User(0, username, password, fullname, email, filename, idioma)

            # Nos devuelve un true si se creó o un false si no
            logged_user = ModelUser.register(self.db, user)

            if type(logged_user) != dict:
                # Lo logeamos con un force True porque debemos forzarlo
                login_user(user=logged_user, force=True)
                data = {'message': '¡Te haz registrado exitosamente!\nTe redirigiremos a la página principal!',
                        'redirectUrl': 'home'}
                
                # Lo redireccionamos a home ya que se ha registrado y lo queremos logear directamente
                return jsonify(data)
            
        except Exception as e:
            raise Exception(e)

        
        return jsonify(logged_user)
