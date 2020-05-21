import asyncio
import json
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, DataError

from app import db
from app.models.users import User
from rabbitmq import queues


user_bp = Blueprint(
    'users', __name__, template_folder='../../templates',
    url_prefix='/users'
)
CORS(user_bp)


def publish(user, token, expire_date):
    loop = asyncio.new_event_loop()
    token_queue = queues.Tokens(loop)

    msg = json.dumps({
        'to': user.email,
        'subject': 'Auth Token',
        'token': token,
        'expire_date': expire_date
    })
    loop.run_until_complete(token_queue.publish(msg.encode()))


def clean_field(value, mask):
    for key_value, replace_value in mask.items():
        value = value.replace(key_value, replace_value)

    return value


@user_bp.route('/', methods=['POST',])
def user():
    mask = {'.': '', '-': ''}

    name = request.json['name']
    email = request.json['email']
    cpf = clean_field(request.json['cpf'], mask)
    rg = clean_field(request.json['rg'], mask)

    try:
        birthdate = (
            datetime.strptime(
                request.json['birthdate'], '%d/%m/%Y'
            ).strftime('%Y-%m-%d')
        )
    except ValueError:
        return jsonify({"error": "Data de nascimento inválida"}), 400

    user = User(
        name=name,
        email=email,
        cpf=cpf,
        rg=rg,
        birthdate=birthdate
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({
            "error": 'Esse email já existe!'
        }), 400
    except DataError:
        return jsonify({
            "error": "Data de nascimento inválida!"
        }), 400

    return jsonify({
        "success": "Usuário cadastrado com successo!"
    }), 200


@user_bp.route('/get_token', methods=['POST',])
def get_token():
    email = request.json.get('email')

    if not email:
        return jsonify({
            'error': 'Email is required'
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            'error': 'User not found'
        }), 400

    token, expire_date = user.generate_token()

    publish(user, token, expire_date)

    return jsonify({'success': 'Token generate!'})


@user_bp.route('/login', methods=['POST',])
def login():
    email = request.json['email']
    token = request.json['token']
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            'error': 'User not found'
        }), 400

    token_valid = token == user.auth_token
    expire = datetime.now() > user.auth_token_expire

    if not token_valid or expire:
        return jsonify({
            'error': 'Invalid token'
        }), 400

    json_user = json.dumps({
        'id': user.id,
        'email': user.email,
        'token': user.auth_token,
        'admin': user.admin
    })

    return jsonify({
        'success': {
            'msg': 'User logged',
        },
        'user': json_user
    })
