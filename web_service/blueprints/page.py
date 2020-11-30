from flask import Blueprint,render_template
from ..model.mariadb import db, Activity, Voice, Url

bp = Blueprint('page', __name__)

@bp.route('/<id>', methods=['GET'])
def activity_page(id):
    id = Url.query.filter_by(hash_code=id).first().activity_id
    return '<html><div id="id"></div></html>'
