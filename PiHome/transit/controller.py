from flask import Blueprint

# Define the blueprint: 'transit', set its url prefix: app.url/auth
from PiHome.transit.model import TransitLog

transit_ctr = Blueprint('transit', __name__, url_prefix='/transit')


@transit_ctr.route('/get?user=<int:user>&fecha_ini=<int:fecha_ini>', methods=['GET'])
@transit_ctr.route('/get?user=<int:user>&fecha_ini=<int:fecha_ini>&fecha_fin=<int:fecha_fin>', methods=['GET'])
def get(**filtro):
    """
    REST que nos devuelve los datos de transito
    :type filtro:
    ['user']        -> Usuario del que nos interesa saber sus tránsitos
    ['fecha_ini']   -> Desde que fecha queremos mostrar
    ['fecha_fin']   -> Hasta que fecha queremos mostrar
    """
    _user = filtro.get('user', None)

    _f_ini = filtro.get('fecha_ini', None)

    _f_fin = filtro.get('fecha_fin', None)

    # transit = TransitLog.query.filter_by(user_id=_user.id, ocurred >= _f_ini, ocurred <= _f_fin).all()
