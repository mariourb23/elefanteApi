from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL
import requests


app = Flask(__name__)

conexion = MySQL(app)

@app.route('/votantes', methods=['GET'])
def listar_votantes():
    try:
        cursor = conexion.connection.cursor()
        sql='SELECT * FROM InformacionVotantes'
        cursor.execute(sql)
        votantes = cursor.fetchall()
        personas=[]
        for fila in votantes:
            votante={
                'Nombre':fila[0],
                'Dpi':fila[1],
                'Departamento':fila[2],
                'Direccion':fila[3],
                'Telefono':fila[4],
                'Transporte':fila[5],
                'Empadronamiento':fila[6],
                'CentroDeVotacion':fila[7],
                'Foto':fila[8],
                'Carnet':fila[9],
                'Rol':fila[10]
            }
            personas.append(votante)
        print(votantes)
        return jsonify({'votantes':personas})
    except Exception as ex:
        return jsonify({'Error': "Error cargando Votantes" })

@app.route('/votantes/<dpi>', methods=['GET'])
def buscar_votante(dpi):
    try:
        cursor = conexion.connection.cursor()
        sql= "SELECT * FROM InformacionVotantes WHERE DPI = '{0}'".format(dpi)
        cursor.execute(sql)
        votante = cursor.fetchone()
        if votante != None:
            persona={
                'Nombre':votante[0],
                'Dpi':votante[1],
                'Carnet':votante[9],
                'Rol':votante[10]
            }
            return jsonify({'votante':persona})
        else:
            return jsonify({'Error': "Votante no encontrado" })
    except Exception as ex:
        return jsonify({'Error': "Error cargando Votante" })
    
@app.route('/votantes', methods=['POST'])
def agregar_votante():
    try:
        cursor = conexion.connection.cursor()
        sql= "SELECT * FROM InformacionVotantes WHERE DPI = '{0}'".format(request.json['Dpi'])
        cursor.execute(sql)
        votante = cursor.fetchone()
        
        if votante != None:
            return jsonify({'Error': "Dpi ya registrado" })
        
        else:
            cursor = conexion.connection.cursor()
            sql =  """INSERT INTO InformacionVotantes (Nombre, DPI, Departamento, Direccion, Telefono, Transporte, Empadronamiento, CentroDeVotacion, Foto, Carnet, Rol) 
            values ('{0}', {1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')""".format(request.json['Nombre'], request.json['Dpi'], request.json['Departamento'], request.json['Direccion'], request.json['Telefono'], request.json['Transporte'], request.json['Empadronamiento'], request.json['CentroDeVotacion'], request.json['Foto'], request.json['Carnet'], request.json['Rol'])
            cursor.execute(sql)
            conexion.connection.commit()
            
            return jsonify({'Mensaje': "Votante registrado" })
    except Exception as ex:
        return jsonify({'Error': "Error cargando Votante" })
    
@app.route('/votantes/<dpi>', methods=['DELETE'])
def eliminar_votante(dpi):
    try:
        cursor = conexion.connection.cursor()
        sql= "DELETE FROM InformacionVotantes WHERE DPI = '{0}'".format(dpi)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Votante eliminado" })
    except Exception as ex:
        return jsonify({'Error': "Error eliminando Votante" })
    
    
@app.route('/votantes/<dpi>', methods=['PUT'])
def actualizar_votante(dpi):
    try:
        cursor = conexion.connection.cursor()
        sql= "SELECT * FROM InformacionVotantes WHERE DPI = '{0}'".format(dpi)
        cursor.execute(sql)
        votante = cursor.fetchone()
        
        if votante != None:
            cursor = conexion.connection.cursor()
            sql =  """UPDATE InformacionVotantes SET Nombre = '{0}', Departamento = '{1}', Direccion = '{2}', Telefono = '{3}', Transporte = '{4}', Empadronamiento = '{5}', CentroDeVotacion = '{6}', Foto = '{7}', Carnet = '{8}', Rol = '{9}' WHERE DPI = '{10}'""".format(request.json['Nombre'], request.json['Departamento'], request.json['Direccion'], request.json['Telefono'], request.json['Transporte'], request.json['Empadronamiento'], request.json['CentroDeVotacion'], request.json['Foto'], request.json['Carnet'], request.json['Rol'], dpi)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'Mensaje': "Votante actualizado" })
        else:
            return jsonify({'Error': "Votante no encontrado" })
    except Exception as ex:
        return jsonify({'Error': "Error actualizando Votante" })

@app.route('/verificar/<dpi>', methods=['GET'])
def verificar_dpi(dpi):
    url = 'https://felgttestaws.digifact.com.gt/gt.com.apinuc/api/Shared?TAXID=000075771500&DATA1=SHARED_GETINFOCUI&DATA2=CUI|{0}&COUNTRY=GT&USERNAME=TESTUSER'.format(dpi)
    print(url)
    try:
        headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VyIjoiR1QuMDAwMDc1NzcxNTAwLlRFU1RVU0VSIiwiQ291bnRyeSI6IkdUIiwiRW52IjoiMCIsIm5iZiI6MTcxMDU0NzEwOCwiZXhwIjoxNzEzMTM5MTA4LCJpYXQiOjE3MTA1NDcxMDgsImlzcyI6Imh0dHBzOi8vd3d3LmRpZ2lmYWN0LmNvbS5ndCIsImF1ZCI6Imh0dHBzOi8vYXBpbnVjLmRpZ2lmYWN0LmNvbS5kby9kby5jb20uYXBpbnVjIn0.JFk6OFA2kXiQgQrbbHXBvdqmE1VlNkFeKtBy83gM5PY'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            nombre = data['RESPONSE'][0]['NOMBRE']
            cui = data['RESPONSE'][0]['CUI']
            nombre_procesado = procesar_nombre(nombre)
            respuesta = {'NOMBRE': nombre_procesado, 'CUI': cui}
            return jsonify(respuesta)
        else:
            return jsonify({'Error': "Error consultando API DPI" })
    except Exception as ex:
        return jsonify({'Error': "Error verificando DPI" })

def procesar_nombre(nombre):
    partes = nombre.split(', ')
    partes = partes[::-1]
    nuevo_nombre = ' '.join(partes)
    
    return nuevo_nombre

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()