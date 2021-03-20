from . import TimeStampMixin, db


class Voice(TimeStampMixin, db.Model):
    __tablename__ = 'voices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
