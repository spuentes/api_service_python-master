'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para administrar la base de datos de registro
de pulsaciones de personas
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

app = Flask(__name__)

# NOTA: Por un bug en el linter de Visual verán problemas con
# el tipo de dato "db". No le den importancia
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

def create_database_app():
    app = Flask(__name__)
    # Recupera database
    dbase, dbase1 = recupera_database()
    print('Entre en Database ', dbase)   
    # Configura SQLAlchemy
    #app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = dbase
    #app.config["SQLALCHEMY_BINDS"] = {'rules': 'sqlite:///testdatabase.db'}
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()
    #return app


class HeartRate(db.Model):
    __tablename__ = "heartrate"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    name = db.Column(db.String)
    value = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Paciente {self.name}, ritmo cardíaco {self.value}"


def insert(time, name, heartrate):
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    engine = sqlalchemy.create_engine(dbase)    
    
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear un nuevo registro de pulsaciones
    pulsaciones = HeartRate(time=time, name=name, value=heartrate)

    # Agregar la persona a la DB
    session.add(pulsaciones)
    session.commit()
    

def report(limit=0, offset=0):
    json_result_list = []

    # Obtener el ultimo registor de cada paciente
    # y ademas la cantidad (count) de registros por paciente
    # Esta forma de realizar el count es más avanzada pero más óptima
    # porque de lo contrario debería realizar una query + count  por persona
    # with_entities --> especificamos que queremos que devuelva la query,
    # por defecto retorna un objeto HeartRate, nosotros estamos solicitando
    # que además devuelva la cantidad de veces que se repite cada nombre
    
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase)
    try:
        engine = sqlalchemy.create_engine(dbase)
        base = declarative_base()

    # Crear la session
        Session = sessionmaker(bind=engine)
        session = Session()
    except:
        print('Error en creacion de engine')

    query = db.session.query(HeartRate).with_entities(HeartRate, db.func.count(HeartRate.name))

    # Agrupamos por paciente (name) para que solo devuelva
    # un valor por paciente
    query = query.group_by(HeartRate.name)

    # Ordenamos por fecha para obtener el ultimo registro
    query = query.order_by(HeartRate.time)

    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    for result in query:
        pulsaciones = result[0]
        cantidad = result[1]
        json_result = {}
        json_result['time'] = pulsaciones.time.strftime("%Y-%m-%d %H:%M:%S.%f")
        json_result['name'] = pulsaciones.name
        json_result['last_heartrate'] = pulsaciones.value
        json_result['records'] = cantidad
        json_result_list.append(json_result)

    return json_result_list

def report1(limit=0, offset=0):
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    stmt = 'SELECT * FROM HeartRate'
    for row in c.execute(stmt):
        json_result = {}
        json_result['time'] = row[1]
        json_result['name'] = row[2]
        json_result['last_heartrate'] = row[3]
        json_result['records'] = row[0]
        json_result_list.append(json_result)
        print(row)

    return json_result_list

def chart(name):

    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase)
    try:
        engine = sqlalchemy.create_engine(dbase)
        base = declarative_base()
    
    # Crear la session
        Session = sessionmaker(bind=engine)
        session = Session()
    except:
        print('Error en creacion de engine')

    # Obtener los últimos 250 registros del paciente
    # ordenado por fecha, obteniedo los últimos 250 registros
    qryname = "'" + name + "'"
    rowcount = db.session.query(HeartRate).filter(HeartRate.name == name).count()
    
    #query = db.session.query(HeartRate).filter(HeartRate.name == name).order_by(HeartRate.time.desc())
    query = db.session.query(HeartRate).with_entities(HeartRate, db.func.count(HeartRate.name))
    query = query.filter(HeartRate.name == name)
    query = query.order_by(HeartRate.time.desc())
    #query = query.limit(250)
    query = query.all()


    #if query_results is None or len(query_results) == 0:
        # No data register
        # Bug a proposito dejado para poner a prueba el traceback
        # ya que el sistema espera una tupla
    #    return []

    # De los resultados obtenidos tomamos el tiempo y las pulsaciones pero
    # en el orden inverso, para tener del más viejo a la más nuevo registro
    #time = [x.time.strftime("%Y-%m-%d %H:%M:%S.%f") for x in reversed(query_results)]
    #heartrate = [x.value for x in reversed(query_results)]
    #return time, heartrate

    json_result_list = []
    for result in query:
        print('Result 0', result[0])
        pulsaciones = result[0]
        cantidad = result[1]
        json_result = {}
        json_result['time'] = pulsaciones.time.strftime("%Y-%m-%d %H:%M:%S.%f")
        json_result['name'] = pulsaciones.name
        json_result['last_heartrate'] = pulsaciones.value
        json_result['records'] = cantidad
        json_result_list.append(json_result)
        print(json_result)
    

    #return time, heartrate
    return json_result_list

def chart1(name):
    # Recupera database
    dbase, dbase1 = recupera_database()

    # Crear el motor (engine) de la base de datos
    print('dbase ', dbase1)
    
    # Establese la conexion a Base de Datos
    conn = sqlite3.connect(dbase1)
    c = conn.cursor()

    # Leer tabla
    json_result_list = []
    time = []
    heartrate = []
    stmt = 'SELECT * FROM HeartRate Where name == "' + name + '"'
    for row in c.execute(stmt):
        time.append(row[1])
        heartrate.append(row[3])
        print(row)

    return time, heartrate

if __name__ == "__main__":
    app = Flask(__name__)
    print("Test del modulo heart.py")
  
    