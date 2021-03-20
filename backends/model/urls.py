from . import TimeStampMixin, db


class Url(TimeStampMixin, db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hash_code = db.Column(db.String(128))
    activity_id = db.Column(db.Integer)

    def __init__(self, hash_code, activity_id):
        self.hash_code = hash_code
        self.activity_id = activity_id
