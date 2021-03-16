from flask import Blueprint, request, url_for, make_response, jsonify
import json
from ..model.mariadb import db, Activity, Voice, Url
from backends.helper.utils import get_short_code
from backends.helper.error import derived_error

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    return json.dumps({'a': 'a', 'b': 'b'})


@bp.route('/activities', methods=['POST'])
def activity_controller():
    name = request.form.get('name', '')
    types = request.form.get('type', '')
    user = request.form.get('user', '')
    intervals = request.form.get('user', 30)
    current_longtitude = request.form.get('current_longtitude', 0)
    current_tatitude = request.form.get('current_latitude', 0)
    end_longtitude = request.form.get('end_longtitude', 0)
    end_tatitude = request.form.get('end_latitude', 0)

    activity = Activity(user, name, intervals, type, current_longtitude,
                        current_tatitude, end_longtitude, end_tatitude)

    db.session.add(activity)
    db.session.flush()

    short_code = get_short_code()
    short_url = Url(short_code, activity.id)

    db.session.add(short_url)
    db.session.commit()

    body = {
        'url': request.host_url  + short_code,
        'activity_id': activity.id,
        **derived_error()
    }

    response = make_response(jsonify(body))
    response.headers['ContentType'] = 'application/json'
    response.status_code = 200

    return response




