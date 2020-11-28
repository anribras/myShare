from flask import Blueprint, request, url_for
import json

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    return json.dumps({'a': 'a', 'b': 'b'})


@bp.route('/activity')
def activity_controller():
    return url_for('.activity_controller', host='666')
