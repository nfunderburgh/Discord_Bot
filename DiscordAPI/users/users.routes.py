from flask import Blueprint
from prayers_controller import read_prayers, create_prayer, update_prayer, delete_prayer

prayers_blueprint = Blueprint('prayers', __name__)

prayers_blueprint.route('/prayers', methods=['GET'])(read_prayers)
prayers_blueprint.route('/prayers', methods=['POST'])(create_prayer)
prayers_blueprint.route('/prayers', methods=['PUT'])(update_prayer)
prayers_blueprint.route('/prayers/<prayerId>', methods=['DELETE'])(delete_prayer)
