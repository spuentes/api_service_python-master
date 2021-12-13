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
import usuario

app = Flask(__name__)


@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h2>Ejercicio Nº1:.. donde id corresponde a userId</h2>"
        result += "<h3>[GET] /user/id/    -----------> mostrar usuario-completados</h3>"
        result += "<h2>Ejercicio Nº2:</h2>"
        result += "<h3>[GET] /user/graph   ----------> mostrar grafico     </h3>"
        result += "<h2>Ejercicio Nº3:</h2>"
        result += "<h3>[GET] /user/titles  ----------> mostrar completados </h3>"
        
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


# ejercicio de practica Nº1
@app.route("/user" , methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        try:
            # Alumno:
            # Implementar la captura de limit y offset de los argumentos
            # de la URL
            # limit = ...
            # offset = ....

            # Debe verificar si el limit y offset son válidos cuando
            # no son especificados en la URL

            # Obtener del HTTP POST JSON el nombre (en minisculas) y los pulsos
            userId = str(request.form.get('userId')).lower()

            if(userId is None):
                # Datos ingresados incorrectos
                    return Response(status=400)

            result = usuario.title_completed_count(userId)
            return jsonify(result)
        except:
            return jsonify({'trace': traceback.format_exc()})
    return ''' 
            <form method="POST">
                <div><label>userId: <input type="text" name="userId"></label></div>
                <input type="submit" value="Submit">
            </form>'''

# ejercicio de practica Nº2
@app.route("/user/titles")
def user_titles():
    try:
        # Obtener el reporte
        result = usuario.reporte()
        return jsonify(result)
    except:
        return jsonify({'trace': traceback.format_exc()})



# ejercicio de practica Nº3
@app.route("/user/graph")
def user_graph():
    try:
        # Alumno:
        # Implementar una función en persona.py llamada "comparativa"
        # Lo que desea es realizar un gráfico de linea con las edades
        # de todas las personas en la base de datos

        # Para eso, su función "dashboard" debe devolver dos valores:
        # - El primer valor que debe devolver es "x", que debe ser
        # los Ids de todas las personas en su base de datos
        # - El segundo valor que debe devolver es "y", que deben ser
        # todas las edades respectivas a los Ids que se encuentran en "x"

        # Descomentar luego de haber implementado su función en persona.py:

        x, y = usuario.comparativa()
        image_html = utils.graficar(x, y)
        return Response(image_html.getvalue(), mimetype='image/png')

        return "Alumno --> Realice la implementacion"
    except:
        return jsonify({'trace': traceback.format_exc()})



#@app.before_first_request
##def before_first_request_func():
#    # Crear aquí todas las bases de datos
#    usuario.conecta_database_app()
#
#    usuario.db.init_app(app)
#
#    # Crear la Base de Datos
#    usuario.db.create_all()
#    #print("Base de datos generada")
#
#    # Carga Tabla - a partir de URL
#    url = 'https://jsonplaceholder.typicode.com/todos'
#    usuario.fill(url)



if __name__ == '__main__':
    print('Inove@Server start!')
    # Crear aquí todas las bases de datos
    usuario.conecta_database_app()

    usuario.db.init_app(app)

    # Crear la Base de Datos
    usuario.db.create_all()
    #print("Base de datos generada")
  
    # Carga Tabla - a partir de URL
    usuario.delete_tabla()
    url = 'https://jsonplaceholder.typicode.com/todos'
    usuario.fill(url)
 
    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
