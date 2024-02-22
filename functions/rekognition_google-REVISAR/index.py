import speech_recognition as sr
import  logging
from pprint import pprint
import boto3 from  botocore.exceptions import ClientError
import  requests

from  rekognition_objects import (RekognitionFace, RekognitionCelebrity, RekognitionLabel,
    RekognitionModerationLabel, RekognitionText, show_bounding_boxes, show_polygons)


# Inicio del punto 1
# Asigan el objeto Recognizer a la variable
r  = sr.Recognizer() 
# Usa el objeto Microphone para escuchar el audio
with
 sr.Microphone() as
source:
   
print('Por
 favor hable: ')
   
# Aloja el audio en la variable audio
   
audio =
r.listen(source)
   
# Usa el bloque try-catch para convertir el audio en texto
   
try:
       
# Aloja el texto del audio en la variable texto
       
texto =
r.recognize_google(audio,
language="es-ES")
       
print('Usted
 dijo: {}'.format(texto))
   
except:
       
print('Lo
 siento, no lo escuche bien. Por favor repita.')
# Final del punto 1


# Inicio del punto 2
# Alojar el cliente AWS en la variable cliente con el servicio de procesamiento de lenguaje
 natural
cliente
 = boto3.client('rekognition',
region_name='us-east-1')
# Devuelve el sentimiento inferido (detectado) de la imagen
response
 = list(cliente.detect_sentiment(Text=texto,
LanguageCode='es').values())
# Despliega la respuestas
print("Respuesta:
 ",
texto,
". ",
response[0])
print("Respuesta
 completa:",
response)
