from flask import render_template
from app.main import bp
from app.entities.Entities import CotacaoTempoReal


@bp.route('/traderexpert/', methods=['GET', 'POST'])
@bp.route('/traderexpert/index', methods=['GET', 'POST'])
def index():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('index.html', title='Home', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])
