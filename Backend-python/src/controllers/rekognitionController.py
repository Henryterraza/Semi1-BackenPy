import os
import json
import boto3
from flask import jsonify, request
from models.file import File
from models.recognition import Recognition
from config.db import get_db
from urllib.parse import unquote

# Configuración de AWS
rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID_REKOGNITION'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_REKOGNITION'),
    region_name=os.getenv('AWS_REGION_REKOGNITION'),
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID_S3"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY_S3"),
    region_name=os.getenv("AWS_REGION_S3"),
)


def imageRecognition():
    db = next(get_db())
    data = request.get_json()
    file_id = data.get('file_id')
    user_id = data.get('user_id')

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
            image_bytes = s3_data['Body'].read()

            rekognition_response = rekognition_client.detect_labels(
                Image={
                    'Bytes': image_bytes,
                }
            )
            # Dividir el texto en partes más pequeñas
            
            recognition_result = json.dumps(rekognition_response)

            # Guardar el resultado en la tabla ImageRecognitionResult
            image_recognition_result = Recognition(
                user_id=user_id,
                file_id=file_id,
                recognition_result=recognition_result
            )

            db.add(image_recognition_result)
            db.commit()

            return jsonify({"result": image_recognition_result.to_dict(), "status": True}), 201


        except Exception as s3_error:
            print('S3 Error:', s3_error)
            return jsonify({"message": "Error al obtener la imagen de S3", "error": str(s3_error), "status": False}), 500

    except Exception as error:
        print('Error in imageRecognition:', error)
        return jsonify({"message": "Error al analizar la imagen", "error": str(error), "status": False}), 500
