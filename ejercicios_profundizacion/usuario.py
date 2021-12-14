#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 2.0

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''


import os
import json
import requests
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
db = SQLAlchemy()

import sqlite3

from config import config

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
environment = config('environment', config_path_name)
database = config('database', config_path_name)

app = Flask(__name__)

# Recupera DataBase - De acuerdo a entorno definido en config.ini
def recupera_database():
    print('script_path ', script_path)
        # Recupera entorno
    typedb = environment.get('modo')
    print('TypeDB :',typedb)

    # recupera database
    if (typedb == 'test'):
        dtabase = database.get('test')    
    if (typedb == 'production'):
        dtabase = database.get('production')

    print("Crea Base de datos")
    dbase = 'sqlite:///{}'.format(dtabase)
    dbase1 = dtabase
    
    return dbase, dbase1


# Establece Conexion - Database
def conecta_database_app():
    app = Flask(__name__)
    # Recupera database
    dbase, dbase1 = recupera_database()
    print('Entre en Database ', dbase)   
    # Configura SQLAlchemy
    #app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = dbase
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()
    #return app


# Define clase - Usuario
class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String)
    completed = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"Usuario: {self.userId}, titulo {self.title}, completado {self.completed} "


# Agrega - Registros en tabla
def insert(userId, title, completed):
    # Recupera database
    dbase, dbase1 = recupera_database()
    # Crear el motor (engine) de la base de datos
    engine = sqlalchemy.create_engine(dbase)    
    
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear una nueva persona
    user = Usuario(userId=userId, title=title, completed=completed)

    # Agregar la persona a la DB
    session.add(user)
    session.commit()


# Elimana - Registros en tabla
def delete_tabla():
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Borra - Tabla
    rowcount = c.execute("DELETE FROM usuario").rowcount

    print('Filas eliminadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


# Recupera Json desde URL
def recupera_jason_url(url):
    # Recibe una URL y devuelve un objeto json_response
    response = requests.get(url)
    dataset = response.json()  

    json_response = dataset
   
    #print('Imprimir los datos traídos de la nube')
    #print(json.dumps(data, indent=4))

    # Vuelca json a archivo XML
    with open('usuario.json', 'w') as jsonfile:
        json.dump(dataset, jsonfile, indent=4)

    return json_response

# Lee - Json
def fetch(json_response):
    # Procesa json_response
    posicion = 0
    for data in json_response:
             
            insert(userId = data['userId'] , title = data['title'], completed = data['completed'])


# Carga - Tabla - a partir de URL
def fill(url):
    fetch(recupera_jason_url(url))
    

# Recupera - Cantidad de ocurrencias
def title_completed_count(userId):
     # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    stmt = 'SELECT * FROM usuario WHERE userId = "' + userId + '" AND completed = 1'
    for row in c.execute(stmt):
        json_result = {}
        json_result['userId'] = row[1]
        json_result['title'] = row[2]
        json_result['completed'] = row[3]
        json_result_list.append(json_result)
        print(row)

    return json_result_list


# Obtiene - Json - Report
def reporte():
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    stmt = 'SELECT * FROM usuario'
    for row in c.execute(stmt):
        json_result = {}
        json_result['userId'] = row[1]
        json_result['title'] = row[2]
        json_result['completed'] = row[3]
        json_result_list.append(json_result)
        print(row)

    return json_result_list


# Obtiene - 2 list - Grafico
def comparativa():
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    userid = []
    completed = []
    stmt = 'SELECT distinct(userId), count(*) FROM usuario WHERE completed = 1 GROUP BY userId'
    for row in c.execute(stmt):
        userid.append(row[0])
        completed.append(row[1])
        print(row)

    return userid, completed

# Main 
if __name__ == "__main__":
    app = Flask(__name__)
    print("Test del modulo usuario.py")

    