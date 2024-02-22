# Funcion lambda que recibe un texto y lo envia al servicio AWS Comprehend para analizarlo
import logging
import json
import boto3
import requests
logger = logging.getLogger()
logger.setLevel(logging.INFO)


comprehend_client = boto3.client('comprehend', region_name='us-east-1')


def lambda_handler(event, context):
    """ Lambda function que analiza los sentimientos de un texto """

    body = event.get('body')

    # Valida que se haya recibido datos en el body.
    if not body:
        raise ValueError('No se recibieron datos en el body.')

    json_body = json.loads(body)
    logger.info(json_body)
    s3_link = json_body.get('s3_link')
    idioma = json_body.get('idioma')

    resultado = "Sin resultado"

    if not s3_link:
        # Llamamos a la funcion de AWS Comprehend    
        resultado = comprehend_client.detect_sentiment(Text=json_body['mensaje'], LanguageCode=idioma)
        logger.info(resultado)
    else:
        transcribe_responde = download_json(s3_link)
        logger.info("Transcribe Responde Download")
        logger.info(transcribe_responde)        
        texto = transcribe_responde['results']['transcripts'][0]['transcript']

        logger.info("Texto")
        logger.info(texto)

        resultado = comprehend_client.detect_sentiment(Text=texto, LanguageCode=idioma)
        logger.info(resultado)

    # Devolvemos el resultado
    return {
        'statusCode': 200,        
        'body': json.dumps(resultado)
    }

# Function to download json file using an url
def download_json(url) -> any:
    """ Function to download json file using an url """
    try:    
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error('Error downloading json file from %s', url)
            return None
    except Exception as e:
        logger.error('Error downloading json file from %s Error %s', url, e)
        return None