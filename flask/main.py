from flask import Flask
from flask_cors import CORS, cross_origin
import os
import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def read_from_data():
    content = []
    data_folder = './data'
    for filename in os.listdir(data_folder):
        with open(os.path.join(data_folder, filename), 'r') as file:
            data = file.read()
            
            content.append(json.loads(data))

    # for filename in os.listdir(data_folder):
    #     os.remove(os.path.join(data_folder, filename))

    return content
