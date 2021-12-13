'''
Flask [Python]
Ejercicios de práctica

Autor: Inove Coding School
Version: 2.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de
las personas registradas.

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''

# Realizar HTTP POST con --> post.py

import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect

import utils
import persona

app = Flask(__name__)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h2>Ejercicio Nº1:</h2>"
        result += "<h3>[GET] /personas?limit=[]&offset=[] --> mostrar el listado de personas (limite and offset are optional)</h3>"
        result += "<h2>Ejercicio Nº2:</h2>"
        result += "<h3>[POST] /registro --> ingresar una nueva persona por JSON, implementar la captura de los valores</h3>"
        result += "<h2>Ejercicio Nº3:</h2>"
        result += "<h3>[GET] /comparativa --> mostrar un gráfico con las edades de todas las personas"
        
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


# ejercicio de practica Nº1
@app.route("/personas")
def personas():
    try:
        # Alumno:
        # Implementar la captura de limit y offset de los argumentos
        # de la URL
        # limit = ...
        # offset = ....
        limit_str = str(request.args.get('limit'))
        offset_str = str(request.args.get('offset'))

        # Debe verificar si el limit y offset son válidos cuando
        # no son especificados en la URL

        limit = 0
        offset = 0

        if(limit_str is not None) and (limit_str.isdigit()):
            limit = int(limit_str)

        if(offset_str is not None) and (offset_str.isdigit()):
            offset = int(offset_str)
        
        # Obtener el reporte
        result = persona.report(limit=limit, offset=offset)
        return jsonify(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


# ejercicio de practica Nº2
@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
        
            # Alumno:
            # Obtener del HTTP POST JSON el nombre y edad
            # name = ...
            # age = ...
            name = str(request.form.get('name')).lower()
            age = str(request.form.get('age'))

            if(name is None or age is None or age.isdigit() is False):
            # Datos ingresados incorrectos
                return Response(status=400)
            
            # Alumno: descomentar la linea persona.insert una vez implementado
            # lo anterior:
            persona.insert(name, age)
            return Response(status=200)
        except:
            return jsonify({'trace': traceback.format_exc()})
    
    return ''' 
            <form method="POST">
                <div><label>name: <input type="text" name="name"></label></div>
                <div><label>age:  <input type="text" name="age"></label></div>
                <input type="submit" value="Submit">
            </form>'''

# ejercicio de practica Nº3
@app.route("/comparativa")
def comparativa():
    try:
        # Alumno:
        # Implementar una función en persona.py llamada "dashboard"
        # Lo que desea es realizar un gráfico de linea con las edades
        # de todas las personas en la base de datos

        # Para eso, su función "dashboard" debe devolver dos valores:
        # - El primer valor que debe devolver es "x", que debe ser
        # los Ids de todas las personas en su base de datos
        # - El segundo valor que debe devolver es "y", que deben ser
        # todas las edades respectivas a los Ids que se encuentran en "x"

        # Descomentar luego de haber implementado su función en persona.py:

        x, y = persona.dashboard()
        image_html = utils.graficar(x, y)
        return Response(image_html.getvalue(), mimetype='image/png')

        return "Alumno --> Realice la implementacion"
    except:
        return jsonify({'trace': traceback.format_exc()})



if __name__ == '__main__':
    print('Inove@Server start!')
    # Crear aquí todas las bases de datos
    persona.conecta_database_app()

    persona.db.init_app(app)

    # Crear la Base de Datos
    persona.db.create_all()
    #print("Base de datos generada")

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
