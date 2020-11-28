from flask import Blueprint, request, url_for
import json
from ..model.mariadb import User,db

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    return json.dumps({'a': 'a', 'b': 'b'})


@bp.route('/activity')
def activity_controller():
    user = User(name="yang")
    db.session.add(user)
    db.session.commit()

    return url_for('.activity_controller', host='666')
