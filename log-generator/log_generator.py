from flask import Flask, jsonify, request
import logging
from logging.handlers import RotatingFileHandler

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Configurar o logging
handler = RotatingFileHandler('/app/logs/app.log', maxBytes=10000000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

@app.route('/')
def index():
    app.logger.info('GET / - Index route accessed')
    return jsonify(message='Welcome to the API!'), 200

@app.route('/status', methods=['GET'])
def status():
    status_code = 200
    app.logger.info('GET /status - Status route accessed with status code %d', status_code)
    return jsonify(status='OK'), status_code

@app.route('/error', methods=['GET'])
def error():
    status_code = 500
    app.logger.error('GET /error - Error route accessed with status code %d', status_code)
    return jsonify(error='Internal Server Error'), status_code

@app.route('/postdata', methods=['POST'])
def postdata():
    data = request.json
    app.logger.info('POST /postdata - Data received: %s', data)
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
