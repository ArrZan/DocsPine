from datetime import timedelta

# Con esta key validaremos ciertas cosas del login
class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
    #Se establece un tiempo para que el usario pueda estar incactivo
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Tiempo de inactividad permitido

# Configuraciones para la conexión de la base de datos local
class DevelopmentConfig(Config):
    DEBUG= True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'
    MYSQL_DB = 'opinion_bd'
    

config = {
    'development' : DevelopmentConfig
}
