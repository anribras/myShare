from . import TimeStampMixin, db
from geoalchemy2.types import Geometry


class Activity(TimeStampMixin, db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(20))
    atype = db.Column(db.Integer)
    name = db.Column(db.String(256))
    to_user = db.Column(db.String(256))
    destination = db.Column(db.String(256))
    left_time = db.Column(db.Time)
    start_poi = db.Column(Geometry(geometry_type='POINT'))
    end_poi = db.Column(Geometry(geometry_type='POINT'))
    current_poi = db.Column(Geometry(geometry_type='POINT'))
    line_poi = db.Column(Geometry(geometry_type='LINESTRING'))

    def __init__(self, u, t, n, to_u, dest, lt, sp, ep, cp, lp):
        self.user = u
        self.atype = t
        self.name = n
        self.to_user = to_u
        self.destination = dest
        self.left_time = lt
        self.start_poi = sp
        self.end_poi = ep
        self.current_poi = cp
        self.line_poi = lp

    def __repr__(self):
        return 'Activity'
