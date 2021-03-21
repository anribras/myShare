from backends.model import db, ma
from marshmallow import post_dump, post_load, pre_dump, pre_load
from marshmallow_sqlalchemy import fields
from backends.model.activites import Activity
import geojson
from geoalchemy2.elements import WKTElement
import shapely
from shapely.geometry import shape

default_point_obj = {
    'coordinates': [-1, 0],
    'type': 'Point'
}
default_linestring_obj = {
    'coordinates': [[-1, 0], [0, 0]],
    'type': 'LineString'
}



class GeoJsonFields(fields.fields.Field):
    """
    1 _deserialize:
    aims: request.json->db
    data-flow:
        geojson obj -> shapely point -> wkt string -> wkt element -> gis db
    function:
          shapely.geometry.shape---->shapely point.wkt --> WKTElement constructor
    2 serialize:
    aims: db->json
    data-flow:
        gis db->wkbelemnt bytes ---> shapely point -> geojson object
    function:
        wkbelement.data.bytes()->shapely.wkb.loads->geojson.Feature 'geometry' attribute.

    """
    def _deserialize(self, value, attr, obj, **kwargs):
        assert value is not None, 'POI null value'
        return WKTElement(shape(value).wkt)

    def _serialize(self, value, attr, obj, **kwargs):
        assert value is not None, 'POI null value'
        shapely_obj= shapely.wkb.loads(value.data.tobytes())
        geojson_obj = geojson.Feature(geometry=shapely_obj)
        return geojson_obj['geometry']


class ActivitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Activity

    @post_dump(pass_many=True)
    def postd_wrap_with_envelope(self, data, many, **kwargs):
        # envelope usage
        return {'data': data}

    @pre_load
    def prel_unwrap_with_envelope(self, data, many, **kwargs):
        return data['data']

    @post_load(pass_many=True)
    def postl_unwrap(self, data, **kwargs):
        if self.context == 'update':
            return data
        else:
            return Activity(**data)

    id = ma.auto_field()
    user = ma.auto_field()
    left_time = ma.auto_field()
    destination = ma.auto_field()
    update_time = ma.auto_field()
    create_time = ma.auto_field()
    atype = ma.auto_field()
    to_user = ma.auto_field()
    # 自定义函数来做Field
    # https://cloud.tencent.com/developer/article/1435948
    # https://marshmallow.readthedocs.io/en/stable/custom_fields.html
    start_poi = GeoJsonFields()
    end_poi = GeoJsonFields()
    current_poi = GeoJsonFields()
    line_poi = GeoJsonFields()
    pass
