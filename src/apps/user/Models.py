from .entities.User import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            # Creamos la conexion a la bd
            cursor=db.connection.cursor()

            # Generamos el script para consultar al usuario
            sql ="""SELECT ID, NombreUsuario, Contraseña FROM usuarios
                    where NombreUsuario = '{}'""".format(user.username)
            
            # Mandamos la consulta a la bd
            cursor.execute(sql)

            # Aquí tendremos nuestro resultado en forma de tupla 
            row = cursor.fetchone()

            #Desconecto de la bd
            cursor.close()

            # Si existe el usuario
            if row != None:
                # Le devolvemos un ojbeto User
                return User(row[0], row[1], User.check_password(user, row[2], user.password))
            else:
                return None

        except Exception as e:
            raise Exception(e)
    
    @classmethod
    def register(self, db, user):
        try:
            # Creamos la conexion a la bd
            cursor=db.connection.cursor()
            
            # Generamos el script para consultar al usuario
            sql = f"""INSERT INTO usuarios
            (IDLenguaje,
            NombreUsuario,
            Contraseña,
            CorreoElectronico,
            NombreCompleto,
            Foto
            )
            VALUES
            (%s, %s, %s, %s, %s, %s);"""
            
            # Hash de la clave
            hashed_pass = User.generate_password(user, user.password)
            
            # Hacer un trigger para la inserción de estos datos y consultar
           # if user.idioma == 'es':
            idLanguage = 1

            # Mandamos la consulta a la bd
            cursor.execute(sql, (idLanguage, user.username, hashed_pass, user.email, user.fullname, user.image))

            # Commiteamos en la bd
            db.connection.commit()

            if cursor.rowcount > 0:
                print('-'*150)
                print('Impresión del ID recién creado: ')
                print(cursor.lastrowid)
                #Desconecto de la bd
                cursor.close()
                # Devolvemos el usuario con su id para logear
                return User(cursor.lastrowid, user.username, hashed_pass)

        except Exception as e:
            # Validamos que el usuario no exista
            if 'Duplicate entry' in str(e) and 'usuarios.NombreUsuario_UNIQUE' in str(e):
                # Deshacemos cambios pendientes
                db.connection.rollback()
                cursor.close()

                data = {'error_message' : f'El nombre de usuario "{user.username}" ya existe.',
                    'redirectUrl': 'register'}
                
                print(data['error_message'])
                
                # La convertimos a json para manejarlo en el frontend
                return data
            
            else:
                db.connection.rollback()
                cursor.close()
                print("Se imprimirá una excepción")
                raise Exception(e)

    
    # Método para obtener los datos y mandarlos a los template
    @classmethod
    def get_by_id(self, db, id):
        try:
            # Creamos la conexion a la bd
            cursor=db.connection.cursor()
            
            # Generamos el script para consultar datos del usuario
            sql ="SELECT ID, NombreUsuario, NombreCompleto, CorreoElectronico, Foto, IDLenguaje FROM usuarios WHERE ID = '{}'".format(id)
            
            # Mandamos la consulta a la bd
            cursor.execute(sql)

            # Aquí tendremos nuestro resultado en forma de tupla 
            row = cursor.fetchone()
            #Desconecto de la bd
            cursor.close()

            # Si existe me devuelve un usuario
            if row != None:
                # Aquí creamos una instancia con los datos que queremos enviar
                return User(id=row[0], username=row[1], password=None, fullname=row[2], email=row[3], image=row[4],idioma=row[5])
            else:
                return None

        except Exception as e:
            raise Exception(e)