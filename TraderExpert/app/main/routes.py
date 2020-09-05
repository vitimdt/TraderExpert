from flask import render_template, request
from app.main import bp
from app.entities.Entities import CotacaoTempoReal, Monitoramento

@bp.route('/traderexpert/', methods=['GET'])
@bp.route('/traderexpert/index', methods=['GET'])
def index():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('index.html', title='Home', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])

@bp.route('/traderexpert/monitor', methods=['GET'])
def monitor():
    cols, rs = Monitoramento.buscaMonitoramentos()
    return render_template('monitoramento.html', title='Monitoramento Ações', columns=cols, items=rs)

@bp.route('/traderexpert/config_monitor', methods=['GET', 'POST'])
def config_monitor():
    titulo = 'Configurar Monitoramento' + str(request.form['monitorSel'])
    return render_template('configMonitoramento.html', title=titulo)
