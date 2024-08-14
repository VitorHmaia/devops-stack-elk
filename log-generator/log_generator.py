import logging
import time
import random
import requests
from logging.handlers import RotatingFileHandler

# Configuração do logging
log_file = '/app/logs/app.log'
handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Funções para gerar logs aleatórios
def generate_random_log():
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    status_codes = [200, 201, 400, 404, 500]
    method = random.choice(methods)
    status_code = random.choice(status_codes)
    message = f'{method} request with status {status_code}'
    return method, status_code, message

# Função para enviar logs para o Logstash
def send_log_to_logstash(method, status_code, message):
    try:
        log_entry = {
            'method': method,
            'status_code': status_code,
            'message': message
        }
        # Enviar logs para o Logstash (ajuste a URL conforme necessário)
        requests.post('http://logstash:5044', json=log_entry)
        logger.info('Sent log entry: %s', log_entry)
    except Exception as e:
        logger.error('Error occurred while sending log: %s', str(e))

def generate_logs():
    while True:
        method, status_code, message = generate_random_log()
        send_log_to_logstash(method, status_code, message)
        time.sleep(2)  # Esperar 2 segundos antes de enviar a próxima requisição

if __name__ == '__main__':
    generate_logs()
