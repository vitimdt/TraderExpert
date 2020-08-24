from flask import render_template
from app.main import bp
from app.entities.Entities import CotacaoTempoReal


@bp.route('/traderexpert/', methods=['GET', 'POST'])
@bp.route('/traderexpert/index', methods=['GET', 'POST'])
def index():
    cols, rs = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('index.html', title='Home', columns=cols, items=rs)
