from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS,cross_origin

from config import config

app = Flask(__name__)

CORS(app)

conexion = MySQL(app)

@cross_origin()
@app.route('/principal', methods=['GET'])
def listar_empleados():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT IdEmple, cedula, nombre, genero, horarioE, horarioS, IdArea, IdCargo FROM empleados"
        cursor.execute(sql)
        datos=cursor.fetchall()
        print(datos)
        empleados=[]
        for fila in datos:
            empleado = {'IdEmple':fila[0],'cedula':fila[1],'nombre':fila[2],'genero':fila[3],'horarioE':fila[4],'horarioS':fila[5],'IdArea':fila[6],'IdCargo':fila[7]}
            empleados.append(empleado)
        return jsonify({'empleado': empleados, 'mensaje': "lista de empleados."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/principal/<IdEmple>', methods=['GET'])
def buscar_empleado(IdEmple):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT IdEmple, cedula, nombre, genero, horarioE, horarioS, IdArea, IdCargo FROM empleados WHERE IdEmple ='{0}'".format(IdEmple)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            empleado = {'IdEmple':datos[0],'cedula':datos[1],'nombre':datos[2],'genero':datos[3], 'horarioE':datos[4], 'horarioS':datos[5],'IdArea':datos[6],'IdCargo':datos[7]}
            return jsonify({'empleado': empleado, 'mensaje': "Empleado encontrado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/principal', methods=['POST'])
def registrar_empleado():
    ##print(request.json)
    try:
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO empleados (IdEmple, cedula, nombre, genero, horarioE, horarioS, IdArea, IdCargo) 
        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')""".format(request.json['IdEmple'],request.json['cedula'],
                                                                     request.json['nombre'],request.json['genero'],
                                                                     request.json['horarioE'],request.json['horarioS'],
                                                                     request.json['IdArea'],request.json['IdCargo'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Empleado Registrado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    
@app.route('/principal/<IdEmple>', methods=['PUT'])
def actualizar_empleado(IdEmple):
    try:
        cursor=conexion.connection.cursor()
        sql= """UPDATE empleados SET horarioE = '{0}', horarioS ='{1}' 
        WHERE IdEmple='{2}'""".format(request.json['horarioE'],request.json['horarioS'],IdEmple)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Empleado Actualizado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/principal/<IdEmple>', methods=['DELETE'])
def eliminar_empleados(IdEmple):
    try:
        cursor=conexion.connection.cursor()
        sql= "DELETE FROM empleados WHERE IdEmple = '{0}'".format(IdEmple)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Empleado Eliminado."})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
    