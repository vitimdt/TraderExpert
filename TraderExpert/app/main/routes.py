from flask import render_template, request, url_for, redirect, flash
from app import db
from app.main import bp
from app.entities.Entities import CotacaoTempoReal, Monitoramento, Carteira
from app.main.forms.configMonitorForm import ConfigMonitorForm
from app.main.forms.monitoramentoForm import MonitoramentoForm
from app.main.forms.carteiraForm import CarteiraForm

@bp.route('/traderexpert/', methods=['GET'])
@bp.route('/traderexpert/index', methods=['GET'])
def index():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('index.html', title='Home', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])

@bp.route('/traderexpert/cotacoestr', methods=['GET'])
def cotacoestr():
    cols, rs, tot = CotacaoTempoReal.buscaCotacaoTR()
    return render_template('_cotacoesTempoReal.html', columns=cols, items=rs,
                           tot_invest=tot[0], tot_cotacao=tot[1], dif_total=tot[2],
                           dif_percentual=tot[3])

@bp.route('/traderexpert/monitor', methods=['GET'])
def monitor():
    form = MonitoramentoForm()
    cols, rs = Monitoramento.buscaMonitoramentos()
    return render_template('monitoramento.html', title='Monitoramento Ações', form=form, columns=cols, items=rs)

@bp.route('/traderexpert/configmonitor', methods=['GET', 'POST'])
def configmonitor():
    monitor_form = ConfigMonitorForm()
    obj_monitoramento = Monitoramento()
    monitoramento = None
    id = "0"
    params = request.args
    if "monitorSel" in params:
        monitorsel = params["monitorSel"]
        if monitorsel != "0":
            id = str(monitorsel).split('_')[1]
        else:
            id = "0"
    if monitor_form.validate_on_submit():
        if id != "0":
            monitoramento = obj_monitoramento.find_by_id(id_monitoramento=int(id))
        else:
            monitoramento = Monitoramento()
        monitoramento.acao_id = monitor_form.acao.data
        monitoramento.valor_ref = monitor_form.valor_ref.data.replace(',', '.')
        monitoramento.operador = monitor_form.operador.data
        monitoramento.valor_meta_dif = monitor_form.valor_dif.data.replace(',', '.')
        monitoramento.sugestao = monitor_form.sugestao.data
        monitoramento.flg_percentual = monitor_form.percentual.data
        monitoramento.flg_ativo = monitor_form.ativo.data
        if id == "0":
            db.session.add(monitoramento)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.configmonitor'))
    elif request.method == 'GET':
        if id != "0":
            monitoramento = obj_monitoramento.find_by_id(id_monitoramento=int(id))
            monitor_form.novo = False
            monitor_form.acao.data = str(monitoramento.acao_id)
            monitor_form.valor_ref.data = str(monitoramento.valor_ref).replace('.', ',')
            monitor_form.operador.data = monitoramento.operador
            monitor_form.valor_dif.data = str(monitoramento.valor_meta_dif).replace('.', ',')
            monitor_form.sugestao.data = monitoramento.sugestao
            monitor_form.percentual.data = monitoramento.flg_percentual
            monitor_form.ativo.data = monitoramento.flg_ativo
    return render_template('configMonitoramento.html', title='Configurar Monitoramento', form=monitor_form)

@bp.route('/traderexpert/todosmonitores', methods=['GET'])
def todosmonitores():
    form = MonitoramentoForm()
    cols, rs = Monitoramento.todosMonitoramentos()
    return render_template('monitores.html', title='Monitoramentos', form=form, columns=cols, items=rs)

@bp.route('/traderexpert/minhacarteira', methods=['GET'])
def minhacarteira():
    form = CarteiraForm()
    cols, rs = Carteira.retornarCarteira()
    return render_template('carteira.html', title='Minha Carteira', form=form, columns=cols, items=rs)

@bp.route('/traderexpert/removeracao', methods=['GET'])
def removeracao():
    id_acao = request.args.get('acaoid')
    itemCarteira = Carteira.query.filter_by(id=id_acao).first_or_404()
    db.session.delete(itemCarteira)
    db.session.commit()
    form = CarteiraForm()
    cols, rs = Carteira.retornarCarteira()
    return render_template('_acoesCarteira.html', form=form, columns=cols, items=rs)
