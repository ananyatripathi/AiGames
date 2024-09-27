from flask import Blueprint, request, jsonify
import app.services.tds_service as tds_service
import app.schemas as schema
from marshmallow import ValidationError
from flask import Blueprint, request, jsonify

tds_bp = Blueprint('tds', __name__)

tds_schema = schema.TDSSchema()

@tds_bp.route('/', methods=['GET'])
def health_check():
    try:
        return jsonify({"Message":"OK"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tds_bp.route('/answer', methods=['POST'])
def ask_suggestion():
    try:
        tds_data = request.get_json()
        validated_tds_data = tds_schema.load(tds_data)
        rounds = validated_tds_data['rounds']
        gender = validated_tds_data['gender']
        age_group = validated_tds_data['age_group']
        playing_with = validated_tds_data['playing_with']
        user_prompt = validated_tds_data['user_prompt']
        prompt = tds_service.get_prompt(rounds=rounds, gender=gender, age_group=age_group, playing_with=playing_with, user_prompt=user_prompt)
        answer = tds_service.get_tds_answer(prompt)
        return jsonify(answer), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

