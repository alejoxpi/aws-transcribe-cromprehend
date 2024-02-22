import boto3 
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

transcribe_client = boto3.client('transcribe', region_name='us-east-1')

def lambda_handler(event, context):
    body = event.get('body')

    # Valida que se haya recibido datos en el body.
    if not body:
        raise ValueError('No se recibieron datos en el body.')
    
    json_body = json.loads(body)
    

    job_name = json_body['job_name']
    logger.info(job_name)

    return get_job(job_name)



def get_job(job_name):
    """
    Gets details about a transcription job.

    :param job_name: The name of the job to retrieve.
    :param transcribe_client: The Boto3 Transcribe client.
    :return: The retrieved transcription job.
    """
    try:
        job = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )

        response = {}        

        status = job['TranscriptionJob']['TranscriptionJobStatus']

        if status == 'COMPLETED':
            logger.info("Download transcript from S3.")
            media_file_uri = job['TranscriptionJob']['Media']['MediaFileUri']
            transcribe_file_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
            response = {
                "status": status,
                "media_file_uri": media_file_uri,
                "transcribe_file_uri": transcribe_file_uri
            }
        else:
            logger.info(f"Not ready yet... Current status is {status}")
            response = {
                "status": status
            }

        return {
            "statusCode": 200,
            "body": json.dumps(response)            
        }        
        
    except ClientError:
        logger.exception("Couldn't get job %s.", job_name)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Couldn't get job."})
        }