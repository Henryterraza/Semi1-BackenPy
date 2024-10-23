from botocore.exceptions import ClientError
import os
import boto3
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename
from models.file import File
from io import BytesIO
from config.db import get_db


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID_S3"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY_S3"),
    region_name=os.getenv("AWS_REGION_S3"),
)


def uploadFile():
    db = next(get_db())
    if "file" not in request.files:
        return jsonify({"message": "Por favor, suba un archivo", "status": False}), 400

    file = request.files["file"]
    # if file.filename == '':
    #     return jsonify({'message': 'El nombre del archivo no puede estar vacío', 'status': False}), 400

    try:
        user_id = request.form.get("user_id")
        if not user_id:
            return (
                jsonify(
                    {"message": "El campo user_id es obligatorio", "status": False}
                ),
                400,
            )

        file_name = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
        file_type = file.mimetype

        s3_path = f"ArchivosUsuarios/{file_name}"

        s3.upload_fileobj(
            file,
            os.getenv("BUCKET_NAME"),
            s3_path,
            ExtraArgs={"ContentType": file_type},
        )

        # Obtener la URL pública del archivo
        s3_url = f"https://{os.getenv('BUCKET_NAME')}.s3.{os.getenv('AWS_REGION_S3')}.amazonaws.com/{s3_path}"

        # Guardar la información del archivo en la base de datos
        new_file = File(
            user_id=user_id, 
            file_name=file_name, 
            file_type=file_type, 
            s3_path=s3_url
        )
        db.add(new_file)  # Guarda el nuevo archivo en la base de datos
        db.commit()  # Guarda los cambios en la base de datos

        return (
            jsonify(
                {
                    "message": "Archivo subido exitosamente",
                    "file": new_file.to_dict(),
                    "status": True,
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error en upload_file: {str(e)}")
        return (
            jsonify(
                {"message": "Error al subir archivo", "error": str(e), "status": False}
            ),
            500,
        )


def getAllFiles():
    db = next(get_db())  
    try:
        files = db.query(File).all()

        files_list = [file.to_dict() for file in files] 

        return jsonify({
            "files": files_list,
            "status": True
        }), 200

    except Exception as e:
        print(f"Error al obtener archivos: {str(e)}")
        return jsonify({
            "message": "Error al obtener archivos",
            "error": str(e),
            "status": False
        }), 500

def getFileById(file_id):
    db = next(get_db())  
  
    try:
        file = db.query(File).filter(File.file_id == file_id).first()

        if not file:
            return jsonify({
                "message": "Archivo no encontrado",
                "status": False
            }), 404

        return jsonify({
            "file": file.to_dict(),  
            "status": True
        }), 200

    except Exception as e:
        print(f"Error al obtener archivo: {str(e)}")
        return jsonify({
            "message": "Error al obtener archivo",
            "error": str(e),
            "status": False
        }), 500
    
def deleteFile(file_id):
    db = next(get_db()) 

    try:
        file = db.query(File).filter(File.file_id == file_id).first()
        
        if not file:
            return jsonify({
                "message": "Archivo no encontrado",
                "status": False
            }), 404

        delete_params = {
            'Bucket': os.getenv('BUCKET_NAME'),
            'Key': f'ArchivosUsuarios/{file.file_name}',  # El nombre con el que se subió
        }

        try:
            s3.delete_object(**delete_params)
        except ClientError as e:
            print(f"Error al eliminar archivo de S3: {str(e)}")
            return jsonify({
                "message": "Error al eliminar archivo de S3",
                "error": str(e),
                "status": False
            }), 500

        # Eliminar registro de la base de datos
        db.delete(file)
        db.commit()

        return jsonify({
            "message": "Archivo eliminado exitosamente",
            "status": True
        }), 200

    except Exception as e:
        print(f"Error al eliminar archivo: {str(e)}")
        return jsonify({
            "message": "Error al eliminar archivo",
            "error": str(e),
            "status": False
        }), 500


def getFilesByUserId(user_id):
    db = next(get_db())  # Obtener la conexión a la base de datos
   
    try:
        # Consultar los archivos por user_id
        files = db.query(File).filter(File.user_id == user_id).all()

        if not files:
            return jsonify({
                "message": "No se encontraron archivos para este usuario",
                "status": False
            }), 404

        return jsonify({
            "files": [file.to_dict() for file in files],  # Asegúrate de que el modelo tenga este método
            "status": True
        }), 200

    except Exception as e:
        print(f"Error al obtener archivos por user_id: {str(e)}")
        return jsonify({
            "message": "Error al obtener archivos",
            "error": str(e),
            "status": False
        }), 500