from flask import Flask, render_template, request, abort, json
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import os
import atexit
import subprocess

USER_KEYS = ['uid', 'nombre', 'nacimiento', 'correo', 'nacionalidad']
MSG_KEYS = ['message', 'sender', 'receptant', 'lat', 'long', 'date']

# Levantamos el servidor de mongo. Esto no es necesario, puede abrir
# una terminal y correr mongod. El DEVNULL hace que no vemos el output
mongod = subprocess.Popen('mongod', stdout=subprocess.DEVNULL)
# Nos aseguramos que cuando el programa termine, mongod no quede corriendo
atexit.register(mongod.kill)

# El cliente se levanta en localhost:5432
client = MongoClient('localhost')
# Utilizamos la base de datos 'entidades'
db = client["entrega4"]
# Seleccionamos la colección de usuarios
mensajes = db.mensajes
usuarios = db.usuarios

# Iniciamos la aplicación de flask
app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>HELLO</h1>"


@app.route("/users1/<int:id>")
def get_info_msg(id):
    lista_mensajes = list(mensajes.find({"id": id},{"_id":0}))
    return json.jsonify(lista_mensajes)

@app.route("/users2/<int:uid>")
def get_info(uid):
    usuario = list(usuarios.find({'uid': uid},{"_id":0}))
    lista_mensajes = list(mensajes.find({'sender': uid},{"_id":0}))
    return  json.jsonify({"usuario": usuario, "mensajes": lista_mensajes})

@app.route("/users3/<int:uid1>/<int:uid2>")
def get_messages(uid1, uid2):
    mensajes_entre = list()
    for mensaje in mensajes.find({"sender": uid1},{"_id":0}):
        if mensaje["receptant"] == uid2:
            mensajes_entre.append({"mensaje":mensaje["message"]})
    for mensaje in mensajes.find({"receptant": uid1},{"_id":0}):
        if mensaje["sender"] == uid2:
            mensajes_entre.append({"mensaje":mensaje["message"]})
    return json.jsonify(mensajes_entre)

mensajes.drop_indexes()
mensajes.create_index([("message", "text")])
@app.route("/users4/<string:frases>")
def msg_frase1(frases):
    frases = frases.split('-')
    resultados_frases = list(mensajes.find({},{"_id":0}))
    for frase in frases:
        nueva_frase = '"' + frase + '"'
        resultado = list(mensajes.find({"$text": {"$search": "'" + nueva_frase + "'"}},{"_id":0}))
        resultados_frases = [x for x in resultado if x in resultados_frases]
    return json.jsonify(resultados_frases)


@app.route("/users5/<string:frases>")
def msg_frase2(frases):
    frases = frases.split('-')
    resultados_frases = list(mensajes.find({},{"_id":0}))
    for frase in frases:
        resultado = list(mensajes.find({"$text": {"$search": "'" + frase + "'"}},{"_id":0}))
        resultados_frases = [x for x in resultado if x in resultados_frases]
    return json.jsonify(resultados_frases)

@app.route("/users6/<string:frases>")
def msg_frase3(frases):
    frases = frases.split('-')
    resultados_frases = list(mensajes.find({},{"_id":0}))
    for frase in frases:
        nueva_frase = '"' + frase + '"'
        resultado = list(mensajes.find({"$text": {"$search": "'" + nueva_frase + "'"}},{"_id":0}))
        resultados_frases = [x for x in resultado if x in resultados_frases]
    resultado_total = list(mensajes.find({},{"_id":0}))
    resultado = [x for x in resultado_total if x not in resultados_frases]
    return json.jsonify(resultado)

@app.route("/users7/<int:uid1>/<int:uid2>", methods=['POST'])
def create_message(uid1, uid2):
    # Si los parametros son enviados con una request de tipo application/json:
    data = {key: request.json[key] for key in MSG_KEYS}
    data["sender"] = uid1
    data["receptant"] = uid2

    # Insertar retorna un objeto
    result = mensajes.insert_one(data)

    # Creo el mensaje resultado
    if (result):
        message = "Mensaje agregado"
        success = True
    else:
        message = "No se pudo agregar el mensaje"
        success = False

    # Retorno el texto plano de un json
    return json.jsonify({'success': success, 'message': message})

@app.route('/users8/<int:id>', methods=['DELETE'])
def delete_message(id):
    # esto borra el primer resultado. si hay mas, no los borra
    mensajes.delete_one({'id': id})

    message = f'Mensaje con id={id} ha sido eliminado.'

    # Retorno el texto plano de un json
    return json.jsonify({'result': 'success', 'message': message})

if os.name == 'nt':
    app.run()
