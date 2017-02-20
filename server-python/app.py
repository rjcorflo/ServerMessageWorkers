""" Web app main
"""
import uuid
import json
import logging
import pika
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient(
    "db",
    27017)
db = client.mydatabase


@app.route('/')
def index():
    """
    Index function
    """
    items = db.tasks.find()
    item_list = [item for item in items]

    return render_template('todo.html', items=item_list)


@app.route('/api/predict', methods=['POST'])
@cross_origin()
def predict():
    """ Ask for prediction
    """
    # Creamos un identificador y lo almacenamos en BBD
    identifier = uuid.uuid4()

    # Recuperamos el JSON de la request
    json_message = request.get_json()

    item_doc = {
        "identifier": str(identifier),
        "status": "PENDING",
        "result": ""
    }

    db.tasks.insert_one(item_doc)
    logging.error("Registro insertado")

    # Adjuntamos el identificador para localizar la tarea desde los workers
    message = {}
    message["identifier"] = str(identifier)
    message["data"] = json_message

    # Mandamos la tarea a la cola
    send_message = json.dumps(message)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="rabbit", port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=send_message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print " [x] Sent task"
    connection.close()

    return jsonify({"identifier": identifier})


@app.route('/api/predict/<id_prediction>', methods=['GET'])
@cross_origin()
def retrieve_predict(id_prediction):
    """
    Recupera el estado de una prediction
    """
    # Recuperamos el item de la BBDD
    items = db.tasks.find({"identifier": str(id_prediction)})

    result = {}
    for item in items:
        result["identifier"] = item["identifier"]
        result["status"] = item["status"]
        result["result"] = item["result"]

    # Devolvemos los datos como JSON
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
