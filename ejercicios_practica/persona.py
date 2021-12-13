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

# Configura nombre aplicacion
app = Flask(__name__)

# Recupera - Database ( De acuerdo a entrono definido en config.ini)
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


# Crea - Database
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


# Define Clase - Persona
class Persona(db.Model):
    __tablename__ = "persona"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Persona:{self.name}, de edad {self.age}"


# Crea - Registro en Tabla
def insert(name, age):
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    engine = sqlalchemy.create_engine(dbase)    
    
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear una nueva persona
    person = Persona(name=name, age=age)

    # Agregar la persona a la DB
    session.add(person)
    session.commit()


# Ejecuta - Reporte
def report(limit=0, offset=0):
        # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    stmt = 'SELECT * FROM persona '
    for row in c.execute(stmt):
        json_result = {'name': row[1], 'age': row[2]}
        json_result_list.append(json_result)
        print(row)

    return json_result_list


# Ejecuta - Dashboard
def dashboard():
        # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    id = []
    age = []
    stmt = 'SELECT * FROM persona '
    for row in c.execute(stmt):
        id.append(row[0])
        age.append(row[2])
        print(row)

    return id, age        

if __name__ == "__main__":
    app = Flask(__name__)
    print("Test del modulo heart.py")

    