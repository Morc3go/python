from flask import Blueprint

adicionar_bp = Blueprint('adicionar', __name__)

@adicionar_bp.route('/adicionar')
def adicionar():
    return 'Página de Adicionar'
