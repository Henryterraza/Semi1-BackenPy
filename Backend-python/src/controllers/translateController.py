import os
import io
import boto3
import pdfplumber
from flask import jsonify, request
from models.file import File
from config.db import get_db
from urllib.parse import unquote

# Configuración de AWS
translate_client = boto3.client(
    'translate',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID_TRASNLATE'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_TRANSLATE'),
    region_name=os.getenv('AWS_REGION_TRANSLATE'),
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID_S3"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY_S3"),
    region_name=os.getenv("AWS_REGION_S3"),
)


def split_text(text, max_size):
    chunks = []
    current_chunk = ''

    for word in text.split(' '):
        if (len(current_chunk.encode('utf-8')) + len(word.encode('utf-8')) + 1 <= max_size):
            current_chunk += (' ' + word) if current_chunk else word  # Añadir la palabra al chunk
        else:
            chunks.append(current_chunk)
            current_chunk = word  


    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def translateDocument():
    db = next(get_db())
    data = request.get_json()
    file_id = data.get('file_id')
    target_language = data.get('target_language')

    try:
        # Buscar el archivo en la base de datos
        file = db.query(File).filter(File.file_id == file_id).first()
        if not file:
            return jsonify({"message": "File not found", "status": False}), 404

        key = file.s3_path.split('.com/')[1]
        decoded_key = unquote(key)
        bucket_name = os.getenv('BUCKET_NAME')

        # Descargar el archivo desde S3
        try:
            s3_data = s3_client.get_object(Bucket=bucket_name, Key=decoded_key)
            content_type = s3_data['ContentType']
            text = ''

            if content_type == 'application/pdf':
                pdf_buffer = s3_data['Body'].read()

                pdf_stream = io.BytesIO(pdf_buffer)
               
                with pdfplumber.open(pdf_stream) as pdf:
                    text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())

            elif content_type == 'text/plain':
                
                text = s3_data['Body'].read().decode('utf-8')
            else:
                return jsonify({"message": "El archivo debe ser un PDF o un archivo de texto", "status": False}), 400

            # Dividir el texto en partes más pequeñas
            
            chunks = split_text(text, 10000)  # 10,000 bytes

            
            translated_chunks = []
            for chunk in chunks:
                translate_response = translate_client.translate_text(
                    Text=chunk,
                    SourceLanguageCode='auto',
                    TargetLanguageCode=target_language
                )
                translated_chunks.append(translate_response['TranslatedText'])

            final_translation = ' '.join(translated_chunks)

            return jsonify({"translatedText": final_translation, "status": True}), 200

        except Exception as s3_error:
            print('S3 Error:', s3_error)
            return jsonify({"message": "Error al obtener archivo de S3", "error": str(s3_error), "status": False}), 500

    except Exception as error:
        print('Error in translateDocument:', error)
        return jsonify({"message": "Error al traducir documento", "error": str(error), "status": False}), 500
