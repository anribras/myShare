from flask import Blueprint, request, make_response, jsonify
import json
import datetime
from backends.model import db, ma
from backends.model.activites import Activity
from backends.model.urls import Url
from backends.helper.utils import get_short_code
from backends.helper.error import derived_error
from flask_restful import Resource, Api
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_AsGeoJSON
import geojson
from backends.helper.error import ErrorCode as E

from marshmallow_sqlalchemy import fields
from .schema import ActivitySchema

bp = Blueprint('public', __name__)
api = Api(bp, catch_all_404s=True)


@bp.route('/')
def index():
    return {
        "nice": "you saw me"
    }


@api.resource('/activity/<int:id>')
class ActivityView(Resource):
    def get(self, id):
        act = db.session.query(Activity).filter_by(id=id).first()
        act_schema = ActivitySchema(exclude=('atype', 'to_user'))
        result = act_schema.dump(act)
        resp = make_response(jsonify(
            **result,
            **derived_error(E.ok)
        ))
        resp.content_type = 'application/json'
        return resp

    def put(self, id):
        # Use context to tell Schema do something special.
        act_schema = ActivitySchema(only=(
            'destination', 'start_poi', 'end_poi', 'current_poi', 'line_poi',
            'left_time', 'update_time'
        ), context='update')

        try:
            act_json = act_schema.load(request.json)
            db.session.query(Activity).filter_by(id=id).update(
                act_json
            )
            db.session.commit()
        except Exception as e:
            if hasattr(e, 'messages'):
                body = {
                    **derived_error(E.input_error, extra=str(e.messages))
                }
            else:
                body = {
                    **derived_error(E.input_error, extra=str(e))
                }
            response = make_response(jsonify(body))
            response.headers['ContentType'] = 'application/json'
            response.status_code = 200
            return response
        response = make_response(jsonify(derived_error(E.ok)))
        response.headers['ContentType'] = 'application/json'
        response.status_code = 200
        return response


@api.resource('/activities')
class ActivitiesView(Resource):
    def post(self):
        act_schema = ActivitySchema(only=(
            'user', 'destination', 'start_poi', 'end_poi', 'current_poi', 'line_poi',
            'left_time', 'atype', 'to_user'
        ))
        try:
            activity = act_schema.load(request.json)
            db.session.add(activity)
            db.session.flush()
        except Exception as e:
            body = {
                **derived_error(E.input_error, extra=str(e.messages))
            }
            response = make_response(jsonify(body))
            response.headers['ContentType'] = 'application/json'
            response.status_code = 200
            return response

        short_code = get_short_code()
        short_url = Url(short_code, activity.id)

        db.session.add(short_url)
        db.session.commit()

        body = {
            'url': request.host_url + short_code,
            'activity_id': activity.id,
            **derived_error(E.ok)
        }

        response = make_response(jsonify(body))
        response.headers['ContentType'] = 'application/json'
        response.status_code = 200
        return response

    def delete(self):
        return {'d': '1'}
        pass
