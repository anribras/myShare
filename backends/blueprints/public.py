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

bp = Blueprint('public', __name__)
api = Api(bp, catch_all_404s=True)


@bp.route('/')
def index():
    return {
        "nice": "you saw me"
    }


# How to jsonify result of sqlalchemy query instance?
# 1. use marsha1 in flask-restful!
# 2. use flask-marshmallow
class ActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Activity

    # new field for geoalchemy2 Geometry conversion
    # start_poi = fields.fields.Method("start_poi_point")

    # convert geoalchemy2 WKTElement object 'POINT(0 0)' into Shapely Point '(0,0)'
    # but can not Serializable to JSON
    #
    def geoJsonLoadsStartPoi(self, obj):
        return geojson.loads(obj.start_poi)

    def geoJsonLoadsEndPoi(self, obj):
        return geojson.loads(obj.end_poi)

    def geoJsonLoadsLinePoi(self, obj):
        return geojson.loads(obj.line_poi)

    id = ma.auto_field()
    user = ma.auto_field()
    left_time = ma.auto_field()
    destination = ma.auto_field()
    start_poi = fields.fields.Method('geoJsonLoadsStartPoi')
    end_poi = fields.fields.Method('geoJsonLoadsEndPoi')
    line_poi = fields.fields.Method('geoJsonLoadsLinePoi')
    pass


@api.resource('/activity/<int:id>')
class ActivityView(Resource):
    def get(self, id):
        # act = db.session.query(Activity).filter_by(id=id).first()
        # act = Activity.query.get(id)
        # I have to Convert WKTElement into GeoJson object in query
        act = db.session.query(
            Activity.id,
            Activity.start_poi.ST_AsGeoJSON(Activity.id).label('start_poi'),
            Activity.end_poi.ST_AsGeoJSON(Activity.id).label('end_poi'),
            Activity.line_poi.ST_AsGeoJSON(Activity.id).label('line_poi'),
            ST_AsGeoJSON(Activity.end_poi),
        ).filter_by(id=id).first()
        act_schema = ActivitySchema()
        result = act_schema.dump(act)
        # query db
        resp = make_response(jsonify(
            **result,
            **derived_error(E.ok)
        ))
        resp.content_type = 'application/json'
        return resp

    def put(self):
        pass


@api.resource('/activities')
class ActivitiesView(Resource):

    def post(self):
        activity = Activity(
            request.form.get('user', 'tester'),
            request.form.get('type', 1),
            request.form.get('name', 'MOSI share'),
            request.form.get('to_user', ''),
            request.form.get('destination', ''),
            request.form.get('left_time', datetime.time()),
            WKTElement(request.form.get('start_poi', 'POINT(0 0)')),
            WKTElement(request.form.get('end_poi', 'POINT(0 0)')),
            WKTElement(request.form.get('current_poi', 'POINT(0 0)')),
            WKTElement(request.form.get('line_poi', 'LINESTRING(0 0,0 0)')),
        )
        db.session.add(activity)
        db.session.flush()

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
