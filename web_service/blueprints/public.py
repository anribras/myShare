from flask import Blueprint, request, url_for, make_response, jsonify
import json
from ..model.mariadb import db, Activity, Voice, Url

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
    db.session.commit()

    response = make_response(jsonify(
        {
            'url': request.host_url + '666',
            'activity_id': activity.id
        })
    )

    response.headers['ContentType'] = 'application/json'
    response.status_code = 200

    return response
