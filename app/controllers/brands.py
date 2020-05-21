import asyncio
import json

from flask import Blueprint, jsonify, request
from flask_cors import CORS

from app import db
from app.models.brands import Brand

from rabbitmq import queues


brand_bp = Blueprint(
    'brands', __name__, template_folder='../../templates',
    url_prefix='/brands'
)
CORS(brand_bp)


def publish(logo_path, logo):
    loop = asyncio.new_event_loop()
    images_queue = queues.Images(loop)

    msg = json.dumps({
        'image': logo,
        'path': logo_path,
    })
    loop.run_until_complete(images_queue.publish(msg.encode()))


def add_brand(name, logo):
    cleaned_name = name.replace(' ', '')
    brand = Brand.query.filter_by(name=name).first()
    logo_path = f'images/logos/{cleaned_name}.jpg'

    if not brand:
        brand = Brand(name=name)

    brand.logo = logo_path

    db.session.add(brand)
    db.session.commit()

    publish(logo_path, logo)

    return brand


@brand_bp.route('/', methods=['GET', 'POST',])
def brands():
    if request.method == 'GET':
        brands = {
            'brands': [{
                'id': brand.id,
                'name': brand.name,
                'logo': brand.logo,
            } for brand in Brand.query.order_by('id')
        ]}

        return jsonify(brands)

    if not request.is_json:
        return jsonify({
            'error': 'Content-type must be json!'
        }), 400

    name = request.json.get('name')
    logo = request.json.get('logo')

    if not name:
        return jsonify({
            'error': 'Brand name is required!'
        }), 400

    if not logo:
        return jsonify({
            'error': 'Brand logo is required!'
        }), 400

    brand = add_brand(name, logo)

    return jsonify({
        'id': brand.id,
        'name': brand.name,
        'logo': brand.logo,
    })

