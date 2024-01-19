from flask import request, jsonify
from typing import List
from prayers_dao import read_prayers, create_prayer, update_prayer, delete_prayer

def read_prayers_handler():
    try:
        prayer_id = int(request.args.get('prayerId', 0))
        print('prayerId', prayer_id)

        prayers = read_prayers()

        return jsonify(prayers), 200

    except Exception as error:
        print('[prayers.controller][read_prayers_handler][Error] ', error)
        return jsonify({'message': 'There was an error when fetching prayers'}), 500

def create_prayer_handler():
    try:
        ok_packet = create_prayer(request.json)

        print('req.json', request.json)
        print('prayer', ok_packet)

        return jsonify(ok_packet), 200

    except Exception as error:
        print('[prayers.controller][create_prayer_handler][Error]', error)
        return jsonify({'message': 'There was an error when writing prayers.'}), 500

def update_prayer_handler():
    try:
        ok_packet = update_prayer(request.json)

        print('req.json', request.json)
        print('prayer', ok_packet)

        return jsonify(ok_packet), 200

    except Exception as error:
        print('[prayers.controller][update_prayer_handler][Error] ', error)
        return jsonify({'message': 'There was an error when updating prayers'}), 500

def delete_prayer_handler(prayer_id):
    try:
        prayer_id = int(prayer_id)
        print('prayer_id', prayer_id)

        if not isinstance(prayer_id, int):
            raise ValueError("Integer expected for prayer_id")

        response = delete_prayer(prayer_id)

        return jsonify(response), 200

    except Exception as error:
        print('[prayers.controller][delete_prayer_handler][Error] ', error)
        return jsonify({'message': 'There was an error when deleting prayers'}), 500
