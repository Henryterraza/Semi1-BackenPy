import os
import boto3
from flask import request, jsonify
from models.user import User
from config.db import get_db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

cognito = boto3.client(
    "cognito-idp",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID_COGNITO"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY_COGNITO"),
    region_name=os.getenv("AWS_REGION_COGNITO"),
)


def createUser():
    db = next(get_db())
    try:

        full_name = request.json.get("full_name")
        email = request.json.get("email")
        password = request.json.get("password")

        if not full_name or not email or not password:
            return jsonify({"message": "Please fill all fields", "status": False}), 400

        email_exists = db.query(User).filter_by(email=email).first()

        if email_exists:
            return jsonify({"message": "Email already exists", "status": False}), 400

        params = {
            "ClientId": os.getenv("COGNITO_CLIENT_ID"),
            "Username": email,
            "Password": password,
            "UserAttributes": [
                {
                    "Name": "email",
                    "Value": email,
                },
                {
                    "Name": "name",
                    "Value": full_name,
                },
            ],
        }

        cognito_response = cognito.sign_up(**params)

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(full_name=full_name, email=email, password=hashed_password)
        db.add(new_user)
        db.commit()

        return (
            jsonify(
                {
                    "message": "Usuario registrado exitosamente",
                    "user": new_user.to_dict(),
                    "cognito_user_id": cognito_response["UserSub"],
                    "status": True,
                }
            ),
            201,
        )

    except Exception as error:
        return (
            jsonify(
                {"message": "Error creating user", "error": str(error), "status": False}
            ),
            500,
        )


def confirmUser():
    try:
        email = request.json.get("email")
        confirmation_code = request.json.get("confirmationCode")

        if not email or not confirmation_code:
            return (
                jsonify(
                    {
                        "message": "Todos los campos son obligatorios: correo electrónico y código de confirmación.",
                        "status": False,
                    }
                ),
                400,
            )

        params = {
            "ClientId": os.getenv("COGNITO_CLIENT_ID"),
            "Username": email,
            "ConfirmationCode": confirmation_code,
        }

        cognito_response = cognito.confirm_sign_up(**params)

        return (
            jsonify(
                {
                    "message": "Usuario confirmado exitosamente",
                    "cognitoResponse": cognito_response,
                    "status": True,
                }
            ),
            200,
        )

    except Exception as error:
        print(f"Error al confirmar usuario: {error}")
        return (
            jsonify(
                {
                    "message": "Error al confirmar usuario",
                    "error": str(error),
                    "status": False,
                }
            ),
            500,
        )


def authUser():
    db = next(get_db())
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        if not email or not password:
            return (
                jsonify(
                    {
                        "message": "El correo electrónico y la contraseña son obligatorios",
                        "status": False,
                    }
                ),
                400,
            )

        user_exists = db.query(User).filter_by(email=email).first()

        if not user_exists:
            return jsonify({"message": "Usuario no encontrado", "status": False}), 404

        match = bcrypt.check_password_hash(user_exists.password, password)

        if not match:
            return jsonify({"message": "Contraseña incorrecta", "status": False}), 400

        return (
            jsonify(
                {
                    "message": "Inicio de sesión exitoso",
                    "user": {
                        "id": user_exists.user_id,
                        "full_name": user_exists.full_name,
                        "email": user_exists.email,
                    },
                    "status": True,
                }
            ),
            200,
        )

    except Exception as error:
        print(f"Error en el login: {error}")
        return (
            jsonify(
                {
                    "message": "Error en el servidor",
                    "error": str(error),
                    "status": False,
                }
            ),
            500,
        )


def getUserProfile(id_user):
    db = next(get_db())
    try:

        user = db.query(User).filter_by(user_id=id_user).first()

        if not user:
            return (
                jsonify(
                    {
                        "message": "Usuario no encontrado",
                        "status": False,
                    }
                ),
                404,
            )
        
        return (
            jsonify(
                {
                    "message": "Perfil del usuario obtenido con éxito",
                    "user": {
                        "id": user.user_id,
                        "full_name": user.full_name,
                        "email": user.email,
                    },
                    "status": True,
                }
            ),
            200,
        )

    except Exception as error:
        print(f"Error al obtener el perfil del usuario: {error}")
        return (
            jsonify(
                {
                    "message": "Error en el servidor",
                    "error": str(error),
                    "status": False,
                }
            ),
            500,
        )

def updateUserProfile(id_user):
    db = next(get_db())
    try:
        full_name = request.json.get("full_name")

        user = db.query(User).filter_by(user_id=id_user).first()

        if not user:
            return (
                jsonify(
                    {
                        "message": "Usuario no encontrado",
                        "status": False,
                    }
                ),
                404,
            )
        
        if full_name:
            user.full_name = full_name

            cognitoParams = {
                "UserAttributes": [
                    {
                        "Name": "name",
                        "Value": full_name,
                    },
                ],
                "UserPoolId": os.getenv("COGNITO_USER_POOL_ID"),
                "Username": user.email,
            }

            cognito.admin_update_user_attributes(**cognitoParams)
        
        db.commit()

        return (
            jsonify(
                {
                    "message": "Perfil actualizado exitosamente",
                    "user": {
                        "id": user.user_id,
                        "full_name": user.full_name,
                        "email": user.email,
                    },
                    "status": True,
                }
            ),
            200,
        )

    except Exception as error:
        print(f"Error al actualizar el perfil del usuario: {error}")
        return (
            jsonify(
                {
                    "message": "Error al actualizar el perfil",
                    "error": str(error),
                    "status": False,
                }
            ),
            500,
        )

def deleteUser(id_user):
    db = next(get_db())
    try:
        user = db.query(User).filter_by(user_id=id_user).first()

        if not user:
            return (
                jsonify(
                    {
                        "message": "Usuario no encontrado",
                        "status": False,
                    }
                ),
                404,
            )
        
        email = user.email


        cognito_params = {
            'UserPoolId': os.getenv('COGNITO_USER_POOL_ID'),
            'Username': email,
        }
        cognito.admin_delete_user(**cognito_params)


        db.delete(user)
        db.commit()

        return (
            jsonify(
                {
                    "message": "Usuario eliminado exitosamente",
                    "status": True,
                }
            ),
            200,
        )

    except Exception as error:
        print(f"Error al eliminar el usuario: {error}")
        return (
            jsonify(
                {
                    "message": "Error al eliminar el usuario",
                    "error": str(error),
                    "status": False,
                }
            ),
            500,
        )