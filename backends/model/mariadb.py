from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backends.helper.utils import get_short_code
db = SQLAlchemy()



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))

class TimeStampMixin(object):
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    delete_at = db.Column(db.DateTime, nullable=True)


class Activity(TimeStampMixin, db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(20), default='')
    atype = db.Column(db.Integer, default=0)
    name = db.Column(db.String(512), default='')
    intervals = db.Column(db.Integer, default=60)
    current_longtitude = db.Column(db.FLOAT)
    current_latitude = db.Column(db.FLOAT)
    end_longtitude = db.Column(db.FLOAT, nullable=True)
    end_latitude = db.Column(db.FLOAT, nullable=True)

    def __init__(self, user, name, intervals, atype, current_longtitude,
                 current_latitude, end_longtitude, end_latitude):
        self.user = user
        self.name = name
        self.intervals = intervals
        self.atypes = atype
        self.current_longtitude = current_longtitude
        self.current_latitude = current_latitude
        self.end_longtitude = end_longtitude
        self.end_latitude = end_latitude

    def __repr__(self):
        return 'Activity'


class Voice(TimeStampMixin, db.Model):
    __tablename__ = 'voices'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(500))
    size = db.Column(db.Integer)
    md5 = db.Column(db.String(128))
    tiny_code = db.Column(db.String(128))
    activity_id = db.Column(db.Integer)

    def __init__(self, name, size, md5, tiny_code, activity_id):
        self.name = name
        self.size = size
        self.md5 = md5
        self.tiny_code = tiny_code
        self.activity_id = activity_id



class Url(TimeStampMixin, db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    hash_code = db.Column(db.String(128))
    activity_id = db.Column(db.Integer)

    def __init__(self, hash_code, activity_id):
        self.hash_code = hash_code
        self.activity_id = activity_id

# modify this in migration/env.py:
    # with connectable.connect() as connection:
    #     context.configure(
    #         connection=connection,
    #         target_metadata=target_metadata,
    #         process_revision_directives=process_revision_directives,
    #         render_as_batch=True, # this line
    #         **current_app.extensions['migrate'].configure_args
    #     )