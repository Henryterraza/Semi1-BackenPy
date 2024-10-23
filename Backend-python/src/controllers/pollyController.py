import os
import io
import boto3
import pdfplumber
import time
from flask import jsonify, request
from models.file import File
from config.db import get_db
from urllib.parse import unquote

# Configuración de AWS Polly y S3
polly_client = boto3.client(
    'polly',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID_POLLY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_POLLY'),
    region_name=os.getenv('AWS_REGION_POLLY'),
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID_S3'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_S3'),
    region_name=os.getenv('AWS_REGION_S3'),
)

def textToSpeech():
    db = next(get_db())
    data = request.get_json()
    file_id = data.get('file_id')
    voice_id = data.get('voice_id', 'Joanna')  # Voz predeterminada

    try:
        # Buscar el archivo en la base de datos
        file = db.query(File).filter(File.file_id == file_id).first()
        if not file:
            return jsonify({"message": "File not found", "status": False}), 404

        # Extraer la clave del s3_path
        key = file.s3_path.split('.com/')[1]
        decoded_key = unquote(key)
        bucket_name = os.getenv('BUCKET_NAME')

        # Descargar el archivo desde S3
        s3_data = s3_client.get_object(Bucket=bucket_name, Key=decoded_key)
        file_body = s3_data['Body'].read()

        text = ''

        # Verificar el tipo de archivo
        file_type = os.path.splitext(file.file_name)[1].lower()
        if file_type == '.pdf':
            # Extraer texto de un PDF usando pdfplumber
            pdf_stream = io.BytesIO(file_body)
            with pdfplumber.open(pdf_stream) as pdf:
                text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif file_type in ['.txt', '.text']:
            # Extraer texto de un archivo de texto
            text = file_body.decode('utf-8')
        else:
            return jsonify({"message": "Unsupported file type", "status": False}), 400

        # Convertir el texto en audio usando Polly
        polly_params = {
            'Text': text,
            'OutputFormat': 'mp3',
            'VoiceId': voice_id,
        }

        audio_response = polly_client.synthesize_speech(**polly_params)

        # Subir el archivo de audio a S3
        audio_file_name = f'AudiosUsuarios/{int(time.time())}_audio.mp3'
        s3_upload_params = {
            'Bucket': bucket_name,
            'Key': audio_file_name,
            'Body': audio_response['AudioStream'],
            'ContentType': 'audio/mpeg',
        }

        s3_client.upload_fileobj(audio_response['AudioStream'], bucket_name, audio_file_name, {'ContentType': 'audio/mpeg'})

        return jsonify({"audioUrl": f'https://{bucket_name}.s3.amazonaws.com/{audio_file_name}', "status": True}), 201

    except Exception as error:
        print('Error in text_to_speech:', error)
        return jsonify({"message": "Error al convertir texto a voz", "error": str(error), "status": False}), 500
