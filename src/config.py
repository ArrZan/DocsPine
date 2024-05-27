import os

# Con esta key validaremos ciertas cosas del login
class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

# Configuraciones para la conexión de la base de datos local
class DevelopmentConfig(Config):
    DEBUG= True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'opinion_bd'
    

config = {
    'development' : DevelopmentConfig
}
