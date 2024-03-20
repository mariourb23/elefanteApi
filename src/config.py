class DevelopmenConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER ='root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'elefanteApp'
    
config = {
    'development': DevelopmenConfig,
}