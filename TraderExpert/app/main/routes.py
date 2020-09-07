from flask import render_template, request, url_for, redirect
from app.main import bp
from app.entities.Entities import CotacaoTempoReal, Monitoramento
from app.main.forms.configMonitorForm import ConfigMonitorForm

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
    titulo = 'ConfigMonitor-' + str(request.form['monitorSel'])
    monitorForm = ConfigMonitorForm()
    if monitorForm.validate_on_submit():
        # current_user.username = form.username.data
        # current_user.about_me = form.about_me.data
        # db.session.commit()
        # flash(_('Your changes have been saved.'))
        return redirect(url_for('main.monitor'))
    elif request.method == 'GET':
        print("GET Tela ConfigMonitor")
        # form.username.data = current_user.username
        # form.about_me.data = current_user.about_me

    return render_template('configMonitoramento.html', title=titulo, form=monitorForm)
