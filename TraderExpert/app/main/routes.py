from flask import render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.main import bp
from app.entities.Entities import CotacaoTempoReal, Monitoramento, Carteira, AcessoAPI, Acao
from app.main.forms.configMonitorForm import ConfigMonitorForm
from app.main.forms.monitoramentoForm import MonitoramentoForm
from app.main.forms.carteiraForm import CarteiraForm
from app.main.forms.acaoCarteiraForm import AcaoCarteiraForm
from app.main.forms.acoesCadastradasForm import AcoesCadastradasForm
from app.main.forms.acaoAcessoForm import AcaoAcessoForm


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


@bp.route('/traderexpert/acoescadastradas', methods=['GET'])
def acoescadastradas():
    form = AcoesCadastradasForm()
    cols, rs = AcessoAPI.retornarAcessosAPI()
    return render_template('acoesCadastradas.html', title='Ações Cadastradas', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/acaoacesso', methods=['GET', 'POST'])
def acaoacesso():
    acaoacesso_form = AcaoAcessoForm()
    obj_acessoApi = AcessoAPI()
    acessoApi = None
    id = "0"
    params = request.args
    if "acessoSel" in params:
        acessoSel = params["acessoSel"]
        if acessoSel != "0":
            id = str(acessoSel).split('_')[1]
        else:
            id = "0"
    if acaoacesso_form.validate_on_submit():
        if id != "0":
            acessoApi = obj_acessoApi.find_by_id(idAcessoAPI=int(id))
        else:
            acessoApi = AcessoAPI()
        acessoApi.acao_id = acaoacesso_form.acao.data
        acessoApi.api_id = acaoacesso_form.API.data
        acessoApi.nome_api = acaoacesso_form.nome_api.data
        if id == "0":
            db.session.add(acessoApi)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.acaoacesso'))
    elif request.method == 'GET':
        if id != "0":
            acessoApi = obj_acessoApi.find_by_id(idAcessoAPI=int(id))
            acaoacesso_form.novo = False
            acaoacesso_form.acao.data = str(acessoApi.acao.id)
            acaoacesso_form.API.data = str(acessoApi.api.id)
            acaoacesso_form.nome_api = str(acessoApi.nome_api)
    return render_template('acaoAcesso.html', title='Configurar Ação e Acesso', form=acaoacesso_form)


@bp.route('/traderexpert/removermonitor', methods=['GET'])
def removermonitor():
    id_monitor = request.args.get('monitorid')
    itemMonitor = Monitoramento.query.filter_by(id=id_monitor).first_or_404()
    db.session.delete(itemMonitor)
    db.session.commit()
    form = MonitoramentoForm()
    cols, rs = Monitoramento.todosMonitoramentos()
    return render_template('_monitores.html', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/minhacarteira', methods=['GET'])
def minhacarteira():
    form = CarteiraForm()
    cols, rs = Carteira.retornarCarteira()
    return render_template('carteira.html', title='Minha Carteira', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/mantercarteira', methods=['GET', 'POST'])
def mantercarteira():
    carteira_form = AcaoCarteiraForm()
    obj_carteira = Carteira()
    acao_carteira = None
    id = "0"
    params = request.args
    if "carteiraSel" in params:
        carteira_sel = params["carteiraSel"]
        if carteira_sel != "0":
            id = str(carteira_sel).split('_')[1]
        else:
            id = "0"
    if carteira_form.validate_on_submit():
        if id != "0":
            acao_carteira = obj_carteira.find_by_id(id_carteira=int(id))
        else:
            acao_carteira = Carteira()
        acao_carteira.acao_id = carteira_form.acao.data
        acao_carteira.email = carteira_form.email.data
        acao_carteira.valor = carteira_form.valor_compra.data.replace(',', '.')
        acao_carteira.quantidade = carteira_form.quantidade.data
        acao_carteira.valor_taxas = carteira_form.valor_taxas.data.replace(',', '.')
        acao_carteira.data_compra = carteira_form.data_compra.data
        acao_carteira.valor_total = carteira_form.valor_total.data.replace(',', '.')
        if id == "0":
            db.session.add(acao_carteira)
        db.session.commit()
        flash('Suas alterações foram gravadas com sucesso.')
        return redirect(url_for('main.mantercarteira'))
    elif request.method == 'GET':
        if id != "0":
            acao_carteira = obj_carteira.find_by_id(id_carteira=int(id))
            carteira_form.acao.data = str(acao_carteira.acao_id)
            carteira_form.email.data = str(acao_carteira.email)
            carteira_form.valor_compra.data = str(acao_carteira.valor).replace('.', ',')
            carteira_form.quantidade.data = acao_carteira.quantidade
            carteira_form.valor_taxas.data = str(acao_carteira.valor_taxas).replace('.', ',')
            carteira_form.data_compra.data = acao_carteira.data_compra
            carteira_form.valor_total.data = str(acao_carteira.valor_total).replace('.', ',')
    return render_template('manterAcaoCarteira.html', title='Manter Carteira', form=carteira_form)


@bp.route('/traderexpert/removeracao', methods=['GET'])
def removeracao():
    id_acao = request.args.get('acaoid')
    itemCarteira = Carteira.query.filter_by(id=id_acao).first_or_404()
    db.session.delete(itemCarteira)
    db.session.commit()
    form = CarteiraForm()
    cols, rs = Carteira.retornarCarteira()
    return render_template('_acoesCarteira.html', form=form, columns=cols, items=rs)


@bp.route('/traderexpert/notifications')
def notifications():
    # Buscar ações sugeridas OK
    cols, rs = Monitoramento.buscaMonitoramentos()
    count = 0
    for row in rs:
        if row['Status'] == 'OK':
            count += 1
    return jsonify([{
        'name': 'acoes_sugeridas',
        'data': str(count)
    }])
