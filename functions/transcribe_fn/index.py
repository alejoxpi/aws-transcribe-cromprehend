# Funcion lambda que recibe un nombre de archivo en S3 y usa el servicio AWS transcribe para extraer el texto
import boto3
import uuid
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
transcribe_client = boto3.client('transcribe', region_name='us-east-1')

def lambda_handler(event, context):
    body = event.get('body')

    # Valida que se haya recibido datos en el body.
    if not body:
        raise ValueError('No se recibieron datos en el body.')
    
    json_body = json.loads(body)
    logger.info(json_body)

    job_name = f"job-{uuid.uuid4()}"
    logger.info(job_name)
    media_uri = json_body['media_uri']
    media_format = json_body['media_format']
    language_code = json_body.get('language_code', 'es-CO')

    job = start_job(job_name, media_uri, media_format, language_code)
    logger.info(job)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'job_name': job_name        
        })
    }

def start_job(
    job_name,
    media_uri,
    media_format,
    language_code="es-CO"    
) -> str:
    
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_uri},
        MediaFormat=media_format,
        LanguageCode=language_code        
    )

    job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    return job    

# {
#     "media_uri": "s3://emociones-transcribe-files/transcribe-sample-1234.mp3",
#     "media_format": "mp3",
#     "language_code": "en-US" 
# }