from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def read_from_data():
    content = []
    data_folder = './data'
    for filename in os.listdir(data_folder):
        with open(os.path.join(data_folder, filename), 'r') as file:
            data = file.read()
            content.append(data)

    for filename in os.listdir(data_folder):
        os.remove(os.path.join(data_folder, filename))
        
    return content
